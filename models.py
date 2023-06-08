from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import os

response_page = Blueprint("response_page", __name__)


def process(prompt):
    file_ext_dict = {}
    uploaded_files = os.listdir("/Users/atikshgupta/Desktop/flask-project/uploaded_files")
    for file_name in uploaded_files:
        if file_name not in file_ext_dict:
            file_ext_dict[file_name] = file_name.split('.')[-1]
    
    loader_array = []
    for file in uploaded_files:
        if file_ext_dict[file] == "pdf":
            loader_array.append(PyPDFLoader("/Users/atikshgupta/Desktop/flask-project/uploaded_files/" + file))
    
    index = VectorstoreIndexCreator().from_loaders(loader_array)
    response = index.query(prompt)

    return response


@response_page.route("/bot_response", methods=["POST", "GET"])
def bot_response():
    loaded_documents = os.listdir("/Users/atikshgupta/Desktop/flask-project/uploaded_files")
    for i, full_filename in enumerate(loaded_documents):
        loaded_documents[i] = full_filename.split(".")[0]

    print(loaded_documents) # not sorted by time yet
    conversation = []

    if request.method == "POST":
        if "user-prompt" in request.form:
            conversation.append(request.form.get("user-prompt"))
            conversation.append(process(request.form.get("user-prompt")))
        elif "right-addfile" in request.form:
            return redirect(url_for("upload"))
    return render_template("QApage.html", conversation=conversation, loaded_documents=loaded_documents)

# THE AI IS STUPID, make it general knowledge + docs, not just docs, it can't even analyse or evaluate the docs so it's kinda useless
