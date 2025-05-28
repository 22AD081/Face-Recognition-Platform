from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains import RetrievalQA
import traceback

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Health check route
@app.route('/')
def home():
    return "RAG Engine is up and running!"

# Load FAISS vectorstore and set up RetrievalQA
try:
    vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings())
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=vectorstore.as_retriever()
    )
except Exception as e:
    print("Error initializing RetrievalQA chain:")
    traceback.print_exc()
    qa = None

@app.route('/ask', methods=['POST'])
def ask():
    if not qa:
        return jsonify({"error": "Vectorstore not loaded"}), 500

    query = request.json.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    result = qa.run(query)
    return jsonify({"answer": result})

if __name__ == '__main__':
    app.run(port=5002)
