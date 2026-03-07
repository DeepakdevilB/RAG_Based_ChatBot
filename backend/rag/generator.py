""" 
This will:

        Accept user question
        Call retrieve_context()
        Format prompt properly
        Send to Azure gpt-4o-mini
        Return final answer
        
        User Question
            ↓
        Retriever → Top 3 chunks
            ↓
        Context injected into GPT
            ↓
        GPT forced to answer only from context
            ↓
        Final response
        
        
For legal / immigration domain, hallucination = dangerous.

So we enforce:
Answer strictly using retrieved context.
If answer not found → say “Information not available in provided documents.”
"""


import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

CHAT_DEPLOYMENT_NAME = "gpt-4o-mini"
API_VERSION = "2025-01-01-preview"

azure_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=API_VERSION,
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def generate_answer(question: str, context: str):

    system_prompt = """
You are an assistant specialized in answering questions about the UK Global Talent Visa.

You will be given context extracted from official documents.

Instructions:
- Use the provided context as the primary source of truth.
- Answer the user's question using the context.
- If multiple pieces of context are relevant, combine them into a clear answer.
- If the context only partially answers the question, provide the available information.
- Do NOT fabricate information that is not supported by the context.
- If the context does not contain the answer, respond exactly with:
  "The information is not available in the provided documents."

Keep responses clear, concise, and helpful.
"""

    user_prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

    response = azure_client.chat.completions.create(
        model=CHAT_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0
    )

    return response.choices[0].message.content