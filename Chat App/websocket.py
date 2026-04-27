# websocket.py
from fastapi import WebSocket

active_connections = {}

async def connect(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket

async def send_message(user_id: int, message: str):
    if user_id in active_connections:
        await active_connections[user_id].send_text(message)
