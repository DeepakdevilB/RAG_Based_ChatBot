"""
What is ingest.py?
Think of it as:
The file that feeds knowledge into your brain (vector database).
Before chatbot can answer anything, it needs data inside ChromaDB.

So ingest.py does:  

                        Raw Website Text(we have provided a PDF for simplicity)
                            ↓
                        Split into chunks
                            ↓
                        Convert chunks → embeddings
                            ↓
                        Store inside ChromaDB
                        
                        
This runs only once (or whenever data updates).
After that, your chatbot just retrieves.
"""

import os
from dotenv import load_dotenv
import chromadb
from pypdf import PdfReader
from openai import AzureOpenAI


import re   # for chunking based on regex pattern - a number followed by a dot

load_dotenv()

PDF_PATH = "data/website_Data_questions.pdf"
CHROMA_PATH = "backend/db/chroma_db"
COLLECTION_NAME = "uk_talent_visa_v2"
CHUNK_SIZE = 800

azure_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def chunk_text(text):

    lines = text.split("\n")
    chunks = []

    current_chunk = ""

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # If line ends with "?" start a new chunk
        if line.endswith("?"):

            if current_chunk:
                chunks.append(current_chunk.strip())

            current_chunk = line

        else:
            current_chunk += " " + line

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def get_embeddings(text_chunks):
    response = azure_client.embeddings.create(
        model="text-embedding-3-small",  # Azure deployment name
        input=text_chunks
    )
    return [item.embedding for item in response.data]

def main():
    print("📄 Loading PDF...")
    text = load_pdf_text(PDF_PATH)

    print("✂️ Chunking text...")
    chunks = chunk_text(text)

    print("🧠 Generating embeddings using Azure...")
    embeddings = get_embeddings(chunks)

    print("🗄️ Setting up ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    print("💾 Storing embeddings in Chroma...")
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(chunks))]
    )

    print("✅ Ingestion complete!")

if __name__ == "__main__":
    main()