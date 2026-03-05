from fastapi import APIRouter, HTTPException
from app.auth.auth_handler import *
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    fake_users_db[user.username] = hash_password(user.password)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: User):
    if user.username not in fake_users_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, fake_users_db[user.username]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token}