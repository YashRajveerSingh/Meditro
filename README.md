# 🩺 Meditro — AI-Powered Medical Assistant

**Meditro** is an AI-powered medical assistant built using **Retrieval-Augmented Generation (RAG)**. It allows users to ask questions about medical information and generates context-aware responses using information retrieved from medical documents.

The application combines **LangChain, Hugging Face Sentence Transformers, Pinecone, PyPDF, Google Generative AI, Gemini 2.5 Flash, and Flask** to build an end-to-end RAG-based question-answering system.

---

## 🚀 Features

* 📄 Upload and process medical PDF documents
* 🔍 Semantic document search using vector embeddings
* 🧠 Retrieval-Augmented Generation (RAG)
* 🤖 AI-powered responses using **Google Gemini 2.5 Flash**
* 🔢 Sentence embeddings using **all-MiniLM-L6-v2**
* 🗄️ Vector storage and similarity search using **Pinecone**
* 🔗 RAG pipeline implemented with **LangChain**
* 🌐 Web interface built with **Flask**
* 📑 PDF document processing using **PyPDF**
* 🔐 API keys managed through environment variables
* 🐳 Docker-ready deployment
* ☁️ Deployable on cloud platforms such as Render or AWS

---

# 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Flask Web App   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ User Question    │
                    └────────┬─────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │      LangChain       │
                 │      RAG Pipeline    │
                 └──────────┬────────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
   ┌─────────────────────┐       ┌─────────────────────┐
   │ Hugging Face        │       │     Pinecone        │
   │ all-MiniLM-L6-v2    │──────▶│  Vector Database    │
   │ Embeddings          │       │ Similarity Search   │
   └─────────────────────┘       └──────────┬──────────┘
                                            │
                                            ▼
                                  ┌─────────────────────┐
                                  │ Retrieved Context   │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │ Gemini 2.5 Flash    │
                                  │ Google Generative AI│
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │     AI Response     │
                                  └─────────────────────┘
```

---

# 🔄 How the RAG Pipeline Works

Meditro follows the following workflow:

### 1. Document Loading

Medical PDF documents are loaded using **PyPDF**.

```text
Medical PDF
     ↓
PyPDF
     ↓
Extracted Text
```

### 2. Text Splitting

The extracted text is divided into smaller chunks using LangChain's text splitter.

This improves retrieval by allowing the system to search smaller and more relevant sections of the document.

```text
Large Document
      ↓
Text Splitting
      ↓
Smaller Chunks
```

### 3. Embedding Generation

Each text chunk is converted into a numerical vector using the Hugging Face model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

These embeddings represent the semantic meaning of the text.

```text
Text Chunk
    ↓
all-MiniLM-L6-v2
    ↓
Vector Embedding
```

### 4. Vector Storage

The generated embeddings are stored in **Pinecone**, which acts as the vector database.

```text
Vector Embeddings
       ↓
    Pinecone
       ↓
Vector Index
```

### 5. Similarity Search

When a user asks a question, the question is converted into an embedding.

Pinecone performs a similarity search to retrieve the most relevant document chunks.

```text
User Question
      ↓
Embedding
      ↓
Pinecone Similarity Search
      ↓
Relevant Context
```

### 6. Context + Question

The retrieved information is combined with the user's question and sent to the LLM.

### 7. Response Generation

**Gemini 2.5 Flash** generates the final response using the retrieved context.

```text
Question + Retrieved Context
              ↓
       Gemini 2.5 Flash
              ↓
         Final Answer
```

---

# 🛠️ Tech Stack

| Technology               | Purpose                            |
| ------------------------ | ---------------------------------- |
| **Python**               | Core programming language          |
| **Flask**                | Web application framework          |
| **LangChain**            | RAG pipeline and LLM orchestration |
| **PyPDF**                | PDF document processing            |
| **Hugging Face**         | Embedding model ecosystem          |
| **all-MiniLM-L6-v2**     | Sentence embeddings                |
| **Pinecone**             | Vector database                    |
| **Google Generative AI** | Gemini integration                 |
| **Gemini 2.5 Flash**     | Large Language Model               |
| **Docker**               | Containerization                   |
| **GitHub**               | Source code management             |

---

# 📂 Project Structure

```text
Meditro/
│
├── app.py
├── store_index.py
├── requirements.txt
├── setup.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
│
├── data/
│   └── medical_documents/
│
├── src/
│   └── ...
│
├── templates/
│   └── ...
│
├── static/
│   └── ...
│
└── .github/
    └── workflows/
        └── cicd.yaml
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YashRajveerSingh/Meditro.git
```

```bash
cd Meditro
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### ⚠️ Security

Never commit your `.env` file to GitHub.

The project uses `.gitignore` to prevent API credentials from being uploaded.

Use `.env.example` as a template:

```env
GEMINI_API_KEY=
PINECONE_API_KEY=
```

---

# 🗄️ Pinecone Configuration

Meditro uses Pinecone for storing and retrieving vector embeddings.

The embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

generates **384-dimensional embeddings**.

Therefore, the Pinecone index should be configured with:

```text
Dimension: 384
Metric: cosine
```

Example:

```text
Index Name: medical-chatbot
Dimension: 384
Metric: cosine
```

---

# ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

Then open:

```text
http://localhost:8080
```

---

# 🐳 Running with Docker

Build the Docker image:

```bash
docker build -t meditro .
```

Run the container:

```bash
docker run -p 8080:8080 --env-file .env meditro
```

Then open:

```text
http://localhost:8080
```

---

# ☁️ Deployment

Meditro is Dockerized and can be deployed to cloud platforms such as:

* Render
* AWS EC2
* AWS ECR
* Other Docker-compatible hosting platforms

A typical deployment architecture is:

```text
GitHub
   ↓
Docker Build
   ↓
Container Registry
   ↓
Cloud Server
   ↓
Meditro
```

---

# 🧠 Why RAG?

A standard LLM may generate answers from its general training knowledge.

Meditro uses **Retrieval-Augmented Generation** to provide the LLM with relevant information retrieved from the configured medical documents.

This allows the application to:

* Ground responses in provided documents
* Retrieve relevant medical information
* Reduce reliance on the model's general knowledge
* Provide context-aware answers

> **Note:** Meditro is an educational/technical project and should not be used as a substitute for professional medical advice, diagnosis, or treatment.

---

# 🔍 Key Components

### LangChain

Used to orchestrate the RAG workflow, including document processing, retrieval, and LLM interaction.

### Hugging Face — all-MiniLM-L6-v2

Used to generate semantic vector representations of text.

```text
Text → 384-dimensional vector
```

### Pinecone

Stores embeddings and performs vector similarity search to retrieve relevant chunks.

### Gemini 2.5 Flash

Used as the generative LLM to produce the final response based on the user's question and retrieved context.

### Flask

Provides the web application/API layer through which users interact with Meditro.

### PyPDF

Extracts text from PDF documents used as the knowledge source.

---

# 📊 RAG Flow

```text
             DOCUMENT INGESTION
                     │
                     ▼
               Medical PDF
                     │
                     ▼
                  PyPDF
                     │
                     ▼
              Text Extraction
                     │
                     ▼
              Text Splitting
                     │
                     ▼
          all-MiniLM-L6-v2
                     │
                     ▼
             Vector Embeddings
                     │
                     ▼
                 Pinecone
                     │
                     │
              VECTOR SEARCH
                     ▲
                     │
              User Question
                     │
                     ▼
          Question Embedding
                     │
                     ▼
                 Pinecone
                     │
                     ▼
            Relevant Chunks
                     │
                     ▼
        Question + Retrieved Context
                     │
                     ▼
             Gemini 2.5 Flash
                     │
                     ▼
              Final Response
```

---

# 🚀 Future Improvements

* Add conversation memory
* Implement authentication
* Add document upload functionality
* Improve citation/source display
* Add evaluation metrics for RAG quality
* Add automated testing
* Add CI/CD deployment pipeline
* Add monitoring and logging
* Add HTTPS with a custom domain
* Implement response guardrails for medical queries

---

# 👨‍💻 Author

**Yash Rajveer Singh**

GitHub:
https://github.com/YashRajveerSingh

---

## ⭐ If you find this project useful

Give the repository a ⭐ on GitHub and feel free to explore the implementation.
