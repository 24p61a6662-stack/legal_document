import ollama
from app.config import LLAMA_MODEL, TEMPERATURE

SYSTEM_PROMPT = """
You are a legal AI assistant specialized in contract analysis.
Provide clause-level analysis, risk categorization, and compliance insights.
Use simple language for non-lawyers.
Always structure responses clearly.
"""

def generate_response(context, query):
    prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nUser Question:\n{query}"
    
    response = ollama.chat(
        model=LLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": TEMPERATURE}
    )
    
    return response["message"]["content"]