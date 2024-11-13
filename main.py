import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory, session, flash, redirect, url_for

import math
import bcrypt
from sympy import randprime

app = Flask(__name__)

def check_session():
    if "username" in session:
        return True
    return False

def mk_hash(password):
    password_b = password.encode("UTF-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_b, salt)
    hashed_str = hashed.decode("UTF-8")
    return hashed_str

def check_password(password, hashed):
    password_b = password.encode("UTF-8")
    return bcrypt.checkpw(password_b, hashed.encode("UTF-8"))

@app.route('/')
def home():
    return render_template('global.html', sess=check_session())

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

@app.route("/upload")
def upload_page():
    return render_template('upload.html')

@app.route("/download")
def download_page():
    data = os.listdir("static/uploads")
    return render_template('download.html', data=data)

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route('/api/change', methods=['POST'])
def change():
    response = {
            "status": 200,
            "text": "成矣"
        }
    if not check_session():
        response = {
            "status": 409,
            "text": "未登之"
        }
        return response
    data = request.json
    path = str(data.get("file"))
    text = str(data.get("text"))
    if os.path.exists(f"repo/{path}"):
        with open(f"repo/{path}", 'r', encoding="UTF-8") as f:
            old_text = f.read()
        with open(f"repo/{path}", 'w', encoding="UTF-8") as f:
            try:
                f.write(text)
            except Exception as e:
                print(e)
                f.write(old_text)
                response['status'] = 500
        return response
    else:
        response = {'status': 405}
        return response

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    response = {
        "status": 200,
        "text": "成矣"
    }
    with open('users.json', 'r') as file:
        users = json.load(file)
    if name in list(users.keys()):
        if check_password(password, users[name]):
            session["username"] = name
        else:
            response["status"] = 409
            response["text"] = "爾秘鍵亦有誤"
    else:
        response["status"] = 409
        response["text"] = "無此名"
    return response

@app.route('/api/signup', methods=['POST'])
def signup():
    response = {
        "status": 200,
        "text": "成矣"
    }
    data = request.get_json()
    name = str(data.get("name"))
    password = str(data.get("password"))
    with open('users.json', 'r') as file:
        users = json.load(file)
    if name in list(data.keys()):
        response["status"] = 409
        response["text"] = "亦有此名之人也"
        return jsonify(response)
    users[name] = mk_hash(password)
    with open("users.json", 'w') as file:
        json.dump(users, file, indent=4)
    return jsonify(response)

@app.route('/api/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('login_page'))

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

@app.route("/api/upload", methods=["POST"])
def upload():
    response = {
        "status": 200,
        "text": "sekses"
    }
    file = request.files["video_file"]
    file.save(f"static/uploads/{file.filename}")
    return response

@app.route("/api/download", methods=["GET"])
def download():
    return send_from_directory("static/uploads", request.args.get("file"), as_attachment=True)

@app.route("/api/check_login", methods=["GET"])
def check_login():
    response = {
        "status": 409,
        "text": "未登也"
    }
    if "username" in session:
        response["status"] = 200
        response["text"] = "登也"
    return jsonify(response)

if __name__ == '__main__':
    app.secret_key = 'dp2898km24'
    app.run(ssl_context=("cert.pem", "key.pem"), host="0.0.0.0", port=4443, debug=True)
