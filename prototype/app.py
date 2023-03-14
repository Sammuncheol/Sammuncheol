import os
from flask import Flask, render_template, request, redirect, send_file, session, flash
from functions import upload_video, get_result, id_duplication_check, login_check, register_member, get_all_video, delete_video, admin_get_all_mem
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'sckey'
UPLOAD_FOLDER = "uploads"
BUCKET = "jolp2076277"
V_TABLE = "jolp2076277"
M_TABLE = "jolpmemtable"

@app.route("/")
def home():
    uid = session.get('uid', None)
    return render_template('main.html', userid=uid)

@app.route("/registerpage")
def registerpage():
    return render_template('registerpage.html')

@app.route("/register", methods=['POST'])
def register():
    if request.method == "POST":
        uid = request.form['id']
        idcheck = id_duplication_check(uid, M_TABLE)
        pw = request.form['pw']
        pwcheck = request.form['pwcheck']
        if not(uid and pw and pwcheck):
            flash("입력되지 않은 값이 있습니다")
            return render_template("registerpage.html")
        elif idcheck == True:
            flash("아이디가 중복됩니다")
            return render_template("registerpage.html")
        elif pw != pwcheck:
            flash("비밀번호가 일치하지 않습니다")
            return render_template("registerpage.html")
        else:
            register_member(uid, pw, M_TABLE)
            flash("회원가입 완료")
    return redirect('/')

@app.route('/login', methods=['POST'])  
def login():
    if request.method == "POST":
        uid = request.form['id']
        pw = request.form['pw']
        login_checked = login_check(uid, pw, M_TABLE)
        if login_checked == True:
            session['uid'] = uid
        else:
            flash("아이디나 비밀번호를 다시 확인하십시오")
            return render_template("main.html")
    return redirect('/')

@app.route('/logout', methods=['GET'])  
def logout():
    session.pop('uid', None)
    return redirect('/')

@app.route("/submit")
def submit():
    uid = session.get('uid', None)
    if not uid:
        flash("로그인하십시오")
        return redirect("/")
    else:
        return render_template('submit.html')

@app.route("/meminfo")
def meminfo():
    uid = session.get('uid', None)
    if not uid:
        flash("로그인하십시오")
        return render_template("main.html")
    else:
        file_names, urls, class_names, upload_times =get_all_video(uid, V_TABLE)
        return render_template('meminfo.html', uid=uid, contents=zip(file_names, urls, class_names, upload_times))

@app.route("/delete", methods=['POST'])
def delete():
    uid = session.get('uid', None)
    if request.method == "POST":
        for key in request.form.getlist('deletecheck'):
            delete_video(key, uid, BUCKET, V_TABLE)
        return redirect("/meminfo")

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        uid = session.get('uid', None)
        file_name = f.filename
        if f:
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            upload_post(f"uploads/{f.filename}", uid, BUCKET, V_TABLE)

        return render_template('loading.html', file_name=file_name, user_id=uid)

@app.route("/result")
def result():
    file_name = request.args.get('file_name', default = 'uploads/conan.png', type=str)
    file_name = "uploads/" + file_name
    user_id = request.args.get('user_id', default = 'user_id', type=str)
    print(file_name, user_id)
    url, class_name = get_result(file_name, user_id, V_TABLE)
    return render_template('result.html', url=url, class_name = class_name)

@app.route("/admin")
def admin():
    uids = admin_get_all_mem(M_TABLE)
    all_information_for_uid = []
    for uid in uids:
        file_names, urls, class_names, upload_times = get_all_video(uid, V_TABLE)
        video_information = [file_names, urls, class_names, upload_items]
        uid_information = [uid, video_information]
        all_information_for_uid.append(uid_information)

    return render_template('admin.html', all_information = all_information_for_uid)

@app.route("/admin_delete", methods=['POST'])
def admin_delete():
    index = []
    if request.method == "POST":
        for key in request.form.getlist('deletecheck'):
            for i in range(len(key)):
                if key[i] == "=":
                    index.append(i)
            file_name = key[index[0]+1:index[1]-5]
            uid = key[index[1]+1:]
            delete_video(file_name, uid, BUCKET, V_TABLE)
    
    return redirect("/admin")

if __name__ == '__main__':
    app.run(debug=True)
