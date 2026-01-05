import os
from openai import OpenAI
from config import MAX_CONTEXT_CHARS
api_key = os.getenv("PERPLEXITY_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("No API key found. Set PERPLEXITY_API_KEY or OPENAI_API_KEY.")

# Perplexity uses OpenAI-compatible client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.perplexity.ai"
)

SYSTEM_PROMPT = """
You are an internal IT support assistant.
Summarize ONLY the provided knowledge base content.
Do NOT add new information.
Do NOT speculate.
If the content does not answer the question, say so.
"""

def summarize_answer(query: str, retrieved_chunks: list[str]) -> str:
    if not retrieved_chunks:
        return "No relevant knowledge base information found."

    context = "\n\n".join(retrieved_chunks)
    context = context[:MAX_CONTEXT_CHARS]

    response = client.chat.completions.create(
        model="sonar-small-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
User question:
{query}

Knowledge base content:
{context}

Provide a concise, factual answer based ONLY on the content above.
"""
            }
        ],
        temperature=0.0,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
