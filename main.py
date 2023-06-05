from flask import Flask
from markupsafe import escape
from flask import request
from flask import url_for
from flask import render_template
from flask import redirect
from werkzeug.utils import secure_filename
from flask import flash
from flask import send_from_directory
import os

UPLOAD_FOLDER = "/Users/atikshgupta/Desktop/flask-project/uploaded_files"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "V3]`AAq#{^t=(99"

@app.route("/login", methods=["GET", "POST"])
def login():
    valid_users = {"admin1": "123"}
    error = None
    if request.method == "POST":
        if request.form["username"] in list(valid_users.keys()) and request.form["password"] == valid_users[request.form["username"]]:
            return redirect(url_for("upload"))
        else:
            error = "invalid credentials"
    
    return render_template("login.html", error=error)


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["GET", "POST"])
def upload():
    upload_complete = None
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part uploaded")
            return redirect(request.url)
        files = request.files.getlist("file")

        for file in files:
            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return redirect(url_for("uploads"))
    return render_template("file_upload.html", upload_complete=upload_complete)



@app.route("/uploads")
def uploads():
    file_ext_dict = {}
    ext_counts = {}
    uploaded_files = os.listdir("/Users/atikshgupta/Desktop/flask-project/uploaded_files")
    for file_name in uploaded_files:
        if file_name not in file_ext_dict:
            file_ext_dict[file_name] = file_name.split('.')[-1]
    
    for extension in list(file_ext_dict.values()):
        if extension in ext_counts:
            ext_counts[extension] += 1
        else:
            ext_counts[extension] = 1
    
    return file_ext_dict

    






if __name__ == '__main__':
    app.run(host='0.0.0.0')