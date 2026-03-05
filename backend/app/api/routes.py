from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta

# ✅ Import RAG function
from app.rag.rag_pipeline import get_rag_response

router = APIRouter()

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

security = HTTPBearer()

# Dummy user
fake_user = {
    "username": "admin",
    "password": "1234"
}

# ---------------------------
# Pydantic models
# ---------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    text: str   # keep this same if frontend sends "text"

class QueryRequest(BaseModel):
    question: str

# ---------------------------
# Login Route
# ---------------------------
@router.post("/login")
def login(data: LoginRequest):
    if data.username != fake_user["username"] or data.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": data.username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

# ---------------------------
# Token Verification
# ---------------------------
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ---------------------------
# Debug Chat Route (No Token Required)
# ---------------------------
@router.post("/chat")
def chat(data: ChatRequest):
    """
    Public RAG route (for testing in frontend).
    """
    answer = get_rag_response(data.text)

    print("Query:", data.text)
    print("Answer:", answer)

    return {
        "answer": answer   # ✅ FIXED (was 'reply')
    }

# ---------------------------
# Protected Ask Route
# ---------------------------
@router.post("/ask")
def ask_question(request: QueryRequest, user=Depends(verify_token)):
    """
    Protected RAG query route. Requires JWT token.
    """
    response = get_rag_response(request.question)

    return {
        "answer": response
    }