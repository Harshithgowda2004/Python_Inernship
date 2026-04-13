from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

posts = []

class Post(BaseModel):
    title: str
    content: str
    author: str
    category: str

@app.get("/posts")
def get_posts():
    return posts

@app.post("/posts")
def create_post(post: Post):
    data = post.dict()
    data["id"] = len(posts) + 1
    data["date"] = str(datetime.now())
    posts.append(data)
    return {"msg": "created"}

@app.get("/posts/{id}")
def get_post(id: int):
    for p in posts:
        if p["id"] == id:
            return p
    return {"error": "not found"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    for i, p in enumerate(posts):
        if p["id"] == id:
            updated = post.dict()
            updated["id"] = id
            updated["date"] = str(datetime.now())
            posts[i] = updated
            return {"msg": "updated"}
    return {"error": "not found"}

@app.delete("/posts/{id}")
def delete_post(id: int):
    global posts
    posts = [p for p in posts if p["id"] != id]
    return {"msg": "deleted"}
