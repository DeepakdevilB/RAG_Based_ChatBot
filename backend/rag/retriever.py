"""
What retriever.py does?
It's like the "search engine" of your chatbot's brain (vector database).
When you ask a question, retriever.py goes into ChromaDB and finds the most relevant pieces of information (chunks) to help answer your question.:
    
    User Question
        ↓
    Generate embedding (Azure)
        ↓
    Query ChromaDB
        ↓
    Return top-k relevant chunks
"""



import os
from dotenv import load_dotenv
import chromadb
from openai import AzureOpenAI

import time         # for measuring latency of retrieval step

load_dotenv()

# -------- CONFIG --------
CHROMA_PATH = "backend/db/chroma_db"
COLLECTION_NAME = "uk_talent_visa_v2"  # must match collection name in ingest.py
TOP_K = 5
# ------------------------

# Azure OpenAI client
azure_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Connect to Chroma
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_collection(name=COLLECTION_NAME)


def get_query_embedding(query: str):
    
    start = time.time()   # Start timer for embedding generation
    
    response = azure_client.embeddings.create(
        model="text-embedding-3-small",  # Azure deployment name
        input=query
    )
    end = time.time()     # End timer for embedding generation
    
    print(f"Embedding Generation Time: {end - start:.3f} seconds")
    
    return response.data[0].embedding


def retrieve_context(query: str, top_k: int = TOP_K):
    query_embedding = get_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]  # return top-k chunks


if __name__ == "__main__":
    # Quick test
    test_query = "What is the eligibilty for UK Talent Visa?"
    docs = retrieve_context(test_query)

    print("\n🔎 Retrieved Documents:\n")
    for i, doc in enumerate(docs):
        print(f"Result {i+1}:\n{doc}\n{'-'*50}")
        
        
        
"""
If later you want more precision:

    Reduce chunk size
    Add overlap between chunks
    Increase top_k
    Use metadata filtering
"""