from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from flask import Blueprint
from flask import render_template
from flask import request

import os

response_page = Blueprint("response_page", __name__)


def process():
    uploaded_files = os.listdir("/Users/atikshgupta/Desktop/flask-project/uploaded_files")
    text = None
    for file in uploaded_files:
        loader = PyPDFLoader("/Users/atikshgupta/Desktop/flask-project/uploaded_files/" + file)
        index = VectorstoreIndexCreator().from_loaders([loader])
        pages = loader.load_and_split()
        query = "what is the essay title"
        response = index.query(query)
    return response

@response_page.route("/bot_response", methods=["POST", "GET"])
def bot_response():
    conversation = []
    count = []
    for i in range(100):
        count.append(i)
    if request.method == "POST":
        print(request)
        conversation.append(request.form.get("user-prompt"))
        conversation.append("Bot response")
    print(request.method)
    return render_template("QApage.html", conversation=conversation, count=count)