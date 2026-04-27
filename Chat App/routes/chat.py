# routes/chat.py
from fastapi import APIRouter
from database import SessionLocal
from models import Message

router = APIRouter()

@router.post("/send")
def send_message(sender_id: int, receiver_id: int, content: str):
    db = SessionLocal()
    msg = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(msg)
    db.commit()
    return {"msg": "Message sent"}

@router.get("/history")
def get_history(user1: int, user2: int):
    db = SessionLocal()
    msgs = db.query(Message).filter(
        ((Message.sender_id == user1) & (Message.receiver_id == user2)) |
        ((Message.sender_id == user2) & (Message.receiver_id == user1))
    ).all()
    return msgs
