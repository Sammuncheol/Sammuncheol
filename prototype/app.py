import os
from flask import Flask, render_template, request, redirect, send_file
from functions import upload_post, get_items
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "jolp2076277"
TABLE = "jolp2076277"

@app.route("/")
def home():
    return render_template('main.html')

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        t = "user_id"
        file_name = f.filename
        if f:
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            upload_post(f"uploads/{f.filename}", tt, BUCKET, TABLE)

        return render_template('loading.html', file_name=file_name, user_id=t)

@app.route("/result")
def result():
    file_name = request.args.get('file_name', default = 'uploads/conan.png', type=str)
    file_name = "uploads/" + file_name
    user_id = request.args.get('user_id', default = 'user_id', type=str)
    print(file_name, user_id)
    url = get_items(file_name, user_id, TABLE)
    return render_template('result.html', url=url, class_name = class_name)

if __name__ == '__main__':
    app.run(debug=True)