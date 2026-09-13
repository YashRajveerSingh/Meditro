from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
from src.prompt import system_prompt

import os


app = Flask(__name__)


# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv(override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Check API keys
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing from .env")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")


# -----------------------------
# Embeddings
# -----------------------------
embeddings = download_hugging_face_embeddings()


# -----------------------------
# Pinecone
# -----------------------------
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)


# -----------------------------
# Retriever
# -----------------------------
retriever = docsearch.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,
        "lambda_mult": 0.5
    }
)


# -----------------------------
# Gemini
# -----------------------------
chatModel = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)


# -----------------------------
# Prompt
# -----------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


# -----------------------------
# Format documents
# -----------------------------
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# -----------------------------
# RAG Chain
# -----------------------------
rag_chain = (
    {
        "context": retriever | format_docs,
        "input": RunnablePassthrough()
    }
    | prompt
    | chatModel
    | StrOutputParser()
)


# -----------------------------
# Home page
# -----------------------------
@app.route("/")
def index():
    return render_template("chat.html")


# -----------------------------
# Chat
# -----------------------------
@app.route("/get", methods=["GET", "POST"])
def chat():

    msg = request.form["msg"]

    print("Question:", msg)

    response = rag_chain.invoke(msg)

    print("Response:", response)

    return str(response)


# -----------------------------
# Run application
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )