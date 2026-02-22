"""
What is ingest.py?
Think of it as:
The file that feeds knowledge into your brain (vector database).
Before chatbot can answer anything, it needs data inside ChromaDB.

So ingest.py does:  

                        Raw Website Text
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
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- CONFIG ----------
DATA_PATH = "data/website_content.txt"
CHROMA_PATH = "backend/db/chroma_db"
COLLECTION_NAME = "uk_talent_visa"
CHUNK_SIZE = 500
# ----------------------------

def load_text():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=CHUNK_SIZE):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

def main():
    print("Loading data...")
    text = load_text()

    print("Chunking data...")
    chunks = chunk_text(text)

    print("Setting up Chroma client...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=openai_ef
    )

    print("Adding chunks to Chroma...")
    collection.add(
        documents=chunks,
        ids=[f"id_{i}" for i in range(len(chunks))]
    )

    print("✅ Data successfully ingested into ChromaDB!")

if __name__ == "__main__":
    main()