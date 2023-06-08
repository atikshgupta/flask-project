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
from models import process, response_page

UPLOAD_FOLDER = "/Users/atikshgupta/Desktop/flask-project/uploaded_files"
ALLOWED_EXTENSIONS = {"txt", "pdf"}

app = Flask(__name__)
app.register_blueprint(response_page)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "V3]`AAq#{^t=(99"

@app.route("/")
def index():
    return redirect(url_for("upload"))

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
    processed_text = None
    for file_name in uploaded_files:
        if file_name not in file_ext_dict:
            file_ext_dict[file_name] = file_name.split('.')[-1]
    
    for extension in list(file_ext_dict.values()):
        if extension in ext_counts:
            ext_counts[extension] += 1
        else:
            ext_counts[extension] = 1
    
    return render_template("uploads.html", file_ext_dict=file_ext_dict)




#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY") #os.getenv("OPENAI_API_KEY")



@app.route("/genfile", methods=["POST", "GET"])
def genfile():
    if request.method == "POST":
        print("ABC: ", request.files)
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
    return render_template("genfile.html")


@app.route("/genform", methods=["POST", "GET"])
def genform():
    if request.method == "POST":
        global personal_details, nett_income, marital_status, family_support, presenting_problems, additional_factors, solutions_tried, prompt_dict, response

        personal_details = request.form.get("personal_details")
        nett_income = request.form.get("nett_income")
        marital_status = request.form.get("marital_status")
        family_support = request.form.get("family_support")
        presenting_problems = request.form.get("presenting_problems")
        additional_factors = request.form.get("additional_factors")
        solutions_tried = request.form.get("solutions_tried")

        prompt_dict = {
            "Personal details": personal_details,
            "Nett income": nett_income,
            "Marital status": marital_status,
            "Family support": family_support,
            "Presenting problems": presenting_problems,
            "Additional factors": additional_factors,
            "Solutions tried": solutions_tried

        }

        form_prompt = "Write a crowdfunding appeal with the following information: "
        for key in list(prompt_dict.keys()):
            form_prompt += f"{key}: {prompt_dict[key]}"
        response = generate_GPT_appeal(form_prompt)
        return redirect(url_for("appeal_display"))
    return render_template("genform.html")



def generate_GPT_appeal(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
            ]
        )
    return completion.choices[0].message["content"]


@app.route("/appeal_display")
def appeal_display():
    return render_template("appeal_display.html", prompt_dict=prompt_dict, generated_appeal=response)






if __name__ == '__main__':
    app.run(port=5000)