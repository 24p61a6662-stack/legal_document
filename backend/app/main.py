from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import PyPDF2
import docx
from PIL import Image
import pytesseract
import io

from app.rag.rag_pipeline import get_rag_response

app = FastAPI()

# ==========================
# ✅ CORS Configuration
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# ✅ Request Model
# ==========================
class ChatRequest(BaseModel):
    question: str


# =====================================================
# 🔥 CHAT ENDPOINT (LEGAL ONLY + RAG CONTROLLED)
# =====================================================
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        question = request.question.lower().strip()

        # 🔒 Legal keyword filter
        legal_keywords = [
            "law", "legal", "contract", "agreement", "clause",
            "nda", "liability", "termination", "employment",
            "compliance", "policy", "regulation", "indemnity",
            "confidential", "breach", "intellectual property",
            "notice period", "arbitration", "jurisdiction"
        ]

        # ✅ Professional Domain Restriction
        if not any(keyword in question for keyword in legal_keywords):
            return {
                "answer": (
                    "Thank you for your query.\n\n"
                    "The submitted question does not fall within the supported "
                    "scope of this system. This Legal Document Assistant is "
                    "specifically designed to provide guidance on legal "
                    "documents, contractual clauses, compliance matters, and "
                    "regulatory topics.\n\n"
                    "Kindly submit a legally relevant question for further assistance."
                )
            }

        # 🧠 Get RAG Response
        response_text = get_rag_response(request.question)

        return {"answer": response_text}

    except Exception as e:
        return {"answer": f"Backend Error: {str(e)}"}


# =====================================================
# 📄 FILE UPLOAD ENDPOINT (PDF / DOCX / IMAGE OCR)
# =====================================================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = ""

        # ================= PDF =================
        if file.filename.endswith(".pdf"):
            pdf = PyPDF2.PdfReader(io.BytesIO(content))
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted

        # ================= DOCX =================
        elif file.filename.endswith(".docx"):
            document = docx.Document(io.BytesIO(content))
            for para in document.paragraphs:
                text += para.text + "\n"

        # ================= IMAGE (OCR) =================
        elif file.filename.endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(image)

        else:
            return {"answer": "Unsupported file format. Please upload PDF, DOCX, or Image files."}

        if text.strip() == "":
            return {"answer": "No readable content found in the uploaded file."}

        # ================= STRICT LEGAL ANALYSIS =================
        system_prompt = """
You are a professional AI Legal Assistant.

STRICT INSTRUCTIONS:
- Analyze strictly from a legal perspective.
- Provide a structured and professional response.
- Do NOT include casual language.
- Do NOT answer unrelated topics.

Format your response as:

1. Document Summary
2. Key Legal Clauses Identified
3. Potential Legal Risks
4. Important Observations
"""

        full_prompt = system_prompt + "\n\nDocument Content:\n" + text

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 600
                }
            },
            timeout=180
        )

        result = response.json()
        return {"answer": result.get("response", "No response generated.")}

    except Exception as e:
        return {"answer": f"File processing error: {str(e)}"}