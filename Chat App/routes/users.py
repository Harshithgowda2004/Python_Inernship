# routes/users.py
from fastapi import APIRouter, Depends
from database import SessionLocal
from models import User
from auth import create_token

router = APIRouter()

@router.post("/register")
def register(username: str, password: str):
    db = SessionLocal()
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    return {"msg": "User created"}

@router.post("/login")
def login(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    if not user or user.password != password:
        return {"error": "Invalid credentials"}

    token = create_token({"sub": user.username})
    return {"access_token": token}
