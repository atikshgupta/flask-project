from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import os
import openai
from pypdf import PdfReader

response_page = Blueprint("response_page", __name__)


def get_documents_text():
    file_ext_dict = {}
    uploaded_files = os.listdir("/Users/atikshgupta/Desktop/flask-project/uploaded_files")
    for file_name in uploaded_files:
        if file_name not in file_ext_dict:
            file_ext_dict[file_name] = file_name.split('.')[-1]
    
    all_docs = []
    for file in uploaded_files:
        if file_ext_dict[file] == "pdf":
            reader = PdfReader("/Users/atikshgupta/Desktop/flask-project/uploaded_files/" + file)
            pages = [page for page in reader.pages]
            pages_text = [page.extract_text() for page in pages]
            full_doc_text = " ".join(pages_text)
            all_docs.append(full_doc_text)

    
    
    

    return all_docs[0] # only works for 1 pdf atm


def chatmode_process(document_text, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are to read the following document, I will ask questions about it: {document_text}. Be very terse and short in your responses"},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    return response["choices"][0]["message"]["content"]




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
            conversation.append(chatmode_process(get_documents_text(), request.form.get("user-prompt")))
        elif "right-addfile" in request.form:
            return redirect(url_for("upload"))
        elif "right-chatmode" in request.form:
            return render_template("QApage.html", conversation=conversation, loaded_documents=loaded_documents, mode="chat mode")
        elif "right-docsmode" in request.form:
            a = get_documents_text()
            return render_template("QApage.html", conversation=conversation, loaded_documents=loaded_documents, mode="docs mode")

    return render_template("QApage.html", conversation=conversation, loaded_documents=loaded_documents, mode="docs mode")

# THE AI IS STUPID, make it general knowledge + docs, not just docs, it can't even analyse or evaluate the docs so it's kinda useless
