import chromadb
from chromadb.utils import embedding_functions
import requests

# -------------------------------
# Configuration
# -------------------------------
MODEL_NAME = "mistral:7b-instruct-q4_0"
MAX_TOKENS = 180
TEMPERATURE = 0.4
TOP_K = 1

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# -------------------------------
# Simple Conversation Memory
# -------------------------------
conversation_memory = {
    "user_name": None,
    "asked_intro": False
}

# -------------------------------
# Chroma Setup
# -------------------------------
chroma_client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = chroma_client.get_collection(
    name="legal_docs",
    embedding_function=embedding_function
)

# -------------------------------
# Ollama Query
# -------------------------------
def query_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": TEMPERATURE,
                    "num_predict": MAX_TOKENS,
                }
            },
            timeout=90
        )

        if response.status_code != 200:
            return "Model error. Ensure Ollama is running."

        return response.json().get("response", "").strip()

    except Exception as e:
        return f"Ollama connection error: {str(e)}"


# -------------------------------
# Friendly Chat Mode
# -------------------------------
def friendly_mode(question: str) -> str:

    name = conversation_memory["user_name"]

    prompt = f"""
You are a friendly, intelligent AI assistant similar to ChatGPT.

User name: {name if name else "Unknown"}

Guidelines:
- Be warm and conversational.
- If greeting, greet politely.
- If user hasn't shared their name, politely ask for it.
- Ask how you can help them.
- Keep response under 100 words.

User:
{question}

Assistant:
"""
    return query_ollama(prompt)


# -------------------------------
# General Legal Mode
# -------------------------------
def general_mode(question: str) -> str:
    prompt = f"""
You are a professional Legal AI Assistant.

Provide:
• 3-5 structured bullet points
• Clear academic explanation
• Short summary at end

Keep under 150 words.

Question:
{question}

Answer:
• 
"""
    return query_ollama(prompt)


# -------------------------------
# Risk Mode
# -------------------------------
def risk_analysis_mode(context: str, question: str) -> str:
    prompt = f"""
You are a Legal Risk Analyst.

Based on context:
• Identify risks
• Explain consequences
• Suggest mitigation

Keep under 150 words.

Context:
{context}

Question:
{question}

Answer:
• 
"""
    return query_ollama(prompt)


# -------------------------------
# Comparison Mode
# -------------------------------
def comparison_mode(context: str, question: str) -> str:
    prompt = f"""
You are a Legal Comparison Expert.

Provide:
• Clause 1 key points
• Clause 2 key points
• Major differences
• Legal impact

Use bullet points.

Context:
{context}

Question:
{question}

Answer:
• 
"""
    return query_ollama(prompt)


# -------------------------------
# Main Smart Assistant Function
# -------------------------------
def get_rag_response(question: str):

    lower_q = question.lower().strip()

    # ---------------------------------
    # Greeting Detection
    # ---------------------------------
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]

    if any(greet in lower_q for greet in greetings):
        conversation_memory["asked_intro"] = True
        return friendly_mode(question)

    # ---------------------------------
    # Capture User Name
    # ---------------------------------
    if "my name is" in lower_q:
        name = question.split("is")[-1].strip()
        conversation_memory["user_name"] = name
        return f"Nice to meet you, {name}! 😊 How can I assist you today?"

    # ---------------------------------
    # Small Talk
    # ---------------------------------
    small_talk = ["how are you", "who are you", "what can you do"]

    if any(talk in lower_q for talk in small_talk):
        return friendly_mode(question)

    # ---------------------------------
    # General Knowledge Mode
    # ---------------------------------
    if any(word in lower_q for word in ["what is", "define", "meaning", "explain"]):
        return general_mode(question)

    # ---------------------------------
    # Retrieve Legal Context
    # ---------------------------------
    results = collection.query(
        query_texts=[question],
        n_results=TOP_K
    )

    if not results.get("documents") or not results["documents"][0]:
        return friendly_mode(question)

    context = "\n\n".join(results["documents"][0])

    # ---------------------------------
    # Risk Mode
    # ---------------------------------
    if "risk" in lower_q:
        return risk_analysis_mode(context, question)

    # ---------------------------------
    # Comparison Mode
    # ---------------------------------
    if "compare" in lower_q or "difference" in lower_q:
        return comparison_mode(context, question)

    # ---------------------------------
    # Default Legal Mode
    # ---------------------------------
    prompt = f"""
You are a professional Legal AI Assistant.

Answer strictly based on context.
Provide bullet points and summary.

Context:
{context}

Question:
{question}

Answer:
• 
"""
    return query_ollama(prompt)