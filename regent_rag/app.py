from flask import Flask, request
from flask_cors import CORS

from regent_rag.retrieval import retrieve_answer

app = Flask(__name__)
CORS(app)


@app.route("/chat", methods=["POST"])
def ask():
    query = request.json["query"]
    result = retrieve_answer(query)
    return {"answer": result["answer"], "sources": result["sources"]}
