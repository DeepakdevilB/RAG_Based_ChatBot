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
from retriever import retrieve_context

load_dotenv()

# -------- CONFIG --------
CHAT_DEPLOYMENT_NAME = "gpt-4o-mini"  # Azure deployment name
API_VERSION = "2025-01-01-preview"
# ------------------------

# Azure client
azure_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=API_VERSION,
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def generate_answer(question: str):
    # Step 1: Retrieve context
    documents = retrieve_context(question)
    context = "\n\n".join(documents)

    # Step 2: Build strict prompt
    system_prompt = """
You are a UK Global Talent Visa assistant.

IMPORTANT RULES:
- Answer ONLY using the provided context.
- Do NOT use outside knowledge.
- If the answer is not found in the context, say:
  "The information is not available in the provided documents."
- Be clear and concise.
"""

    user_prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

    # Step 3: Call Azure GPT
    response = azure_client.chat.completions.create(
        model=CHAT_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0  # very important for strict factual answers
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    test_question = "Can students apply for UK Talent Visa?"
    answer = generate_answer(test_question)

    print("\n🤖 Final Answer:\n")
    print(answer)