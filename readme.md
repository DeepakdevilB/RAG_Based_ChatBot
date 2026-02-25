# UK Global Talent Visa RAG Chatbot

An AI-powered chatbot built using Azure OpenAI, ChromaDB, FastAPI, and a custom Retrieval-Augmented Generation (RAG) pipeline.

This system answers questions strictly based on provided UK Global Talent Visa documentation, ensuring grounded and non-hallucinated responses.

---

## 🚀 Features

- Azure OpenAI Embeddings (`text-embedding-3-small`)
- Azure OpenAI Chat Model (`gpt-4o-mini`)
- ChromaDB persistent vector database
- Strict context-based answering (No hallucination)
- FastAPI backend with REST endpoint
- Clean HTML/CSS/JS frontend
- Modular RAG architecture

---

## 🧠 Architecture

PDF Data
↓
Azure Embeddings (text-embedding-3-small)
↓
ChromaDB (Persistent Vector Store)
↓
Retriever (Semantic Search)
↓
Generator (gpt-4o-mini)
↓
FastAPI (/chat endpoint)
↓
Frontend UI



---

## 📁 Project Structure

backend/
│
├── main.py # FastAPI entry point
├── rag/
│ ├── ingest.py # PDF ingestion & embedding storage
│ ├── retriever.py # Semantic search layer
│ ├── generator.py # Grounded answer generation
│ └── pipeline.py # RAG orchestration layer
│
└── db/ # ChromaDB storage (ignored in git)

frontend/
├── index.html
├── style.css
└── script.js

.env # Environment variables (not committed)
requirements.txt
README.md


Setup Instructions - 


1️⃣ Clone the Repository
git clone <your-repo-url>
cd <project-folder>



2️⃣ Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Mac / Linux
python3 -m venv venv
source venv/bin/activate



3️⃣ Install Dependencies
pip install -r requirements.txt




4️⃣ Configure Environment Variables

Create a .env file in the project root:

AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_OPENAI_API_VERSION=2023-05-15

⚠️ Do NOT commit .env to GitHub.

Make sure .gitignore contains:

.env
venv/
backend/db/chroma_db/
__pycache__/




5️⃣ Ingest the Data (Important Step)

Before running the server, generate embeddings and store them in ChromaDB:

python backend/rag/ingest.py

This will:

Extract text from PDF

Generate embeddings using Azure OpenAI

Store vectors in ChromaDB

You should see:

Ingestion complete!



6️⃣ Run the Backend Server
uvicorn backend.main:app --reload

Server will start at:

http://127.0.0.1:8000

Swagger Docs available at:

http://127.0.0.1:8000/docs


7️⃣ Test API

Use Swagger UI or send request:

POST /chat

Request Body:

{
  "message": "What is the minimum age?"
}


8️⃣ Run Frontend

Open:

frontend/index.html

