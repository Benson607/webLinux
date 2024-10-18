import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('global.html')

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
            return render_template('git_view.html', path=f"{path}", files=" ".join(files), text="")
        else:
            with open(f"repo/{path}", 'r') as f:
                file = ""
                dir_path = path
                while 1:
                    if dir_path[-1] == '/':
                        break
                    file = dir_path[-1] + file
                    dir_path = dir_path[:-1]
                files = os.listdir(f"repo/{dir_path}")
                return render_template('git_view.html', path=f"{dir_path}", file = file, files=" ".join(files), text=f.read())

@app.route('/api/change', methods=['POST'])
def change():
    data = request.json
    path = data.get("file")
    text = data.get("text")
    if os.path.exists(f"repo/{path}"):
        response = {'status': 200}
        with open(f"repo/{path}", 'r') as f:
            old_text = f.read()
        with open(f"repo/{path}", 'w') as f:
            try:
                f.write(text)
            except:
                f.write(old_text)
                response['status'] = 500
        return jsonify(response)
    else:
        response = {'status': 405}
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)