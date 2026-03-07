""" 
CURRENT STRCUTURE :
        PDF → Embeddings → Chroma

        User Question
        ↓
        Retriever
        ↓
        Generator
        ↓
        Answer
       
After adding pipeline: 
        User Question
        ↓
        rag_pipeline()
        ↓
        Retriever
        ↓
        Generator
        ↓
        Answer
        
Why This Is Important (Professional Reason)

When you build FastAPI, your endpoint should not know about:

        Chroma
        Azure
        Embeddings
        Context injection
        Prompt engineering

It should just do:

@app.post("/chat")
def chat(request):
    return rag_pipeline(request.message)

That’s clean separation of concerns.
"""

from .retriever import retrieve_context
from .generator import generate_answer

import time         # for measuring latency of entire pipeline  


def rag_pipeline(question: str, top_k: int = 5):
    
    total_start = time.time()   # Start timer for entire pipeline

    # Step 1: Retrieve relevant chunks
    retrieval_start = time.time()   # Start timer for retrieval
    documents = retrieve_context(question, top_k=top_k)
    retrieval_end = time.time()     # End timer for retrieval
    
    """Debugging code (to check retrieved chunks from ChromaDB)- for production comment this out"""
    for i, doc in enumerate(documents):
        print(f"\n--- Chunk {i+1} ---\n")
        print(doc)
        print("\n------------------------------------\n")
    
    
    context = "\n\n".join(documents)

    # Step 2: Generate final answer
    llm_start = time.time()   # Start timer for LLM generation
    answer = generate_answer(question, context)
    llm_end = time.time()     # End timer for LLM generation
    
    total_end = time.time()   # End timer for entire pipeline
    
    # -------- Print Latency --------
    print("\n=========== LATENCY REPORT ===========")

    print(f"Retrieval Time: {retrieval_end - retrieval_start:.3f} seconds")
    print(f"LLM Generation Time: {llm_end - llm_start:.3f} seconds")
    print(f"Total Pipeline Time: {total_end - total_start:.3f} seconds")

    print("======================================\n")
    
    return answer


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        response = rag_pipeline(question)
        print("\n🤖 Answer:\n")
        print(response)