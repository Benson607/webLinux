import os
import json
from flask import Flask, render_template, request, jsonify

import math
import bcrypt
from sympy import randprime

def are_coprime(a, b):
    return math.gcd(a, b) == 1

def secret():
    p = randprime(2 ** 1023, 2 ** 1024 - 1)
    q = randprime(2 ** 1023, 2 ** 1024 - 1)
    while p % q == 0 or q % p == 0:
        p = randprime(2 ** 1023, 2 ** 1024 - 1)
        q = randprime(2 ** 1023, 2 ** 1024 - 1)
    n = p * q
    fin = (p - 1) * (q - 1)
    e = 65537
    while not are_coprime(e, fin):
        e += 1
    k = 1
    while (fin * k + 1) % e != 0:
        k += 1
    d = (fin * k + 1) // e
    return n, e, d

def resecret(num_hex):
    print("recive")
    with open("key", 'r') as f:
        key = int(f.read())
    with open("modn", 'r') as f:
        n = int(f.read())

    num_int = int(num_hex, 16)
    num_b = bin(pow(num_int, key, n))[2:]
    print(num_b)
    while len(num_b) < 64:
        num_b = '0' + num_b
    num_str = ""
    print(num_b)
    for i in range(0, len(num_b), 8):
        num_str = num_str + chr(int(num_b[i:i+8], 2))
        print(num_b[i:i+8])

    print(num_str)

    return num_str

def mk_hash(password):
    password_b = password.encode("UTF-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_b, salt)
    hashed_str = hashed.decode("UTF-8")
    return hashed_str

def check_password(password, hashed):
    password_b = password.encode("UTF-8")
    return bcrypt.checkpw(password_b, hashed.encode("UTF-8"))

def set_key():
    modn, pub_key, key = secret()
    with open("key", 'w') as f:
        f.write(str(key))
    with open("pub_key", 'w') as f:
        f.write(str(pub_key))
    with open("modn", 'w') as f:
        f.write(str(modn))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('global.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/gitlab')
def gitlab():
    repos_list = os.listdir("repo")
    return render_template('myGitLab.html', repos = " ".join(repos_list))

@app.route('/view_git')
def viwe_git():
    path = request.args.get("path")
    if os.path.exists(f"repo/{path}"):
        if os.path.isdir(f"repo/{path}"):
            files = os.listdir(f"repo/{path}")
            if path[-1] != '/':
                path = path + '/'
            return render_template('git_view.html', path=f"{path}", files=" ".join(files), text="", file_type="")
        else:
            with open(f"repo/{path}", 'r', encoding="UTF-8") as f:
                file = ""
                dir_path = path
                while 1:
                    if dir_path[-1] == '/':
                        break
                    file = dir_path[-1] + file
                    dir_path = dir_path[:-1]
                files = os.listdir(f"repo/{dir_path}")
                file_type = ""
                if ".cpp" in file:
                    file_type = "cpp"
                elif ".c" in file:
                    file_type = "c"
                elif ".java" in file:
                    file_type = "java"
                elif ".js" in file:
                    file_type = "javascripts"
                elif ".md" in file:
                    file_type = "markdown"
                elif ".json" in file:
                    file_type = "json"
                elif ".py" in file:
                    file_type = "python"
                elif ".html" in file:
                    file_type = "html"
                return render_template('git_view.html', path=f"{dir_path}", file = file, files=" ".join(files), text=f.read(), file_type=file_type)

@app.route('/api/change', methods=['POST'])
def change():
    data = request.json
    path = str(data.get("file"))
    text = str(data.get("text"))
    if os.path.exists(f"repo/{path}"):
        response = {'status': 200}
        with open(f"repo/{path}", 'r', encoding="UTF-8") as f:
            old_text = f.read()
        with open(f"repo/{path}", 'w', encoding="UTF-8") as f:
            try:
                f.write(text)
            except Exception as e:
                print(e)
                f.write(old_text)
                response['status'] = 500
        return jsonify(response)
    else:
        response = {'status': 405}
        return jsonify(response)

@app.route('/api/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    return 0

@app.route('/api/signup', methods=['POST'])
def signup():
    response = {
        "status": 200,
        "text": "成矣"
    }
    data = request.json
    name = str(data.get("name"))
    password = str(data.get("password"))
    with open('users.json', 'r') as file:
        data = json.load(file)
    if name in list(data.keys()):
        response["status"] = 409
        response["text"] = "亦有此名之人也"
        return jsonify(response)
    password = resecret(password)
    data[name] = mk_hash(password)
    with open("users.json", 'w') as file:
        json.dump(data, file, indent=4)
    return jsonify(response)

@app.route("/api/get_key")
def get_pub_key():
    with open("modn", 'r') as f:
        modn = hex(int(f.read()))
    with open("pub_key", 'r') as f:
        pub_key = hex(int(f.read()))
    response = {
        "modn": modn,
        "pub_key": pub_key
    }
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
