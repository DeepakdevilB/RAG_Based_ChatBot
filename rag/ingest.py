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
from chromadb.utils import embedding_functions
from pypdf import PdfReader

# Load environment variables
load_dotenv()

# -------- CONFIG --------
PDF_PATH = "data/website_Data_questions.pdf"
CHROMA_PATH = "backend/db/chroma_db"
COLLECTION_NAME = "uk_talent_visa"
CHUNK_SIZE = 800   # Slightly bigger chunks for PDF
# ------------------------

def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    return text


def chunk_text(text, chunk_size=CHUNK_SIZE):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks


def main():
    print("📄 Loading PDF...")
    text = load_pdf_text(PDF_PATH)

    print("✂️ Chunking text...")
    chunks = chunk_text(text)

    print("🧠 Setting up ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=openai_ef
    )

    print("💾 Storing embeddings in Chroma...")
    collection.add(
        documents=chunks,
        ids=[f"doc_{i}" for i in range(len(chunks))]
    )

    print("✅ Ingestion complete! Vector DB ready.")


if __name__ == "__main__":
    main()