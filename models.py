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


def get_documents_dict():
    file_ext_dict = {}
    file_names = []
    uploaded_files = os.listdir("/Users/atikshgupta/Desktop/flask-project/uploaded_files")
    for file_name in uploaded_files:
        file_names.append(file_name)
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
    
    file_names_and_contents = {}
    for i in range(len(file_names)):
        file_names_and_contents[uploaded_files[i]] = all_docs[i]
    
    print(file_names_and_contents)

    return file_names_and_contents # only works for 1 pdf atm


def chatmode_process(prompt):
    all_docs_in_a_dict = get_documents_dict()
    docs_names = list(all_docs_in_a_dict.keys())
    doc_dict = {"role": "user", "content": f"Document 1 — name: {docs_names[0]}, content: {all_docs_in_a_dict[docs_names[0]]}"}
    doc_dict_list = [doc_dict]
    for i in range(1, len(docs_names)):
        new = doc_dict.copy()
        new["content"] = f"Document {i} — name: {docs_names[i]}, content: {all_docs_in_a_dict[docs_names[i]]}"
        doc_dict_list.append(new)
    
    messages = [d for d in doc_dict_list]
    messages.insert(0, {"role": "system", "content": f"You are to read the following documents, I will ask questions about them. Be very terse and short in your responses"})

    print(messages)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
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
            conversation.append(chatmode_process(request.form.get("user-prompt")))
        elif "right-addfile" in request.form:
            return redirect(url_for("upload"))
        elif "right-chatmode" in request.form:
            return render_template("QApage.html", conversation=conversation, loaded_documents=loaded_documents, mode="chat mode")
        elif "right-docsmode" in request.form:
            return render_template("QApage.html", conversation=conversation, loaded_documents=loaded_documents, mode="docs mode")

    return render_template("QApage.html", conversation=conversation, loaded_documents=loaded_documents, mode="docs mode")

# THE AI IS STUPID, make it general knowledge + docs, not just docs, it can't even analyse or evaluate the docs so it's kinda useless
