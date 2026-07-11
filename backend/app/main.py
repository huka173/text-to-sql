from fastapi import FastAPI

from app.services.chat_service import process_question
from app.services.wren_service import execute_sql
from app.schemas.chat import ChatRequest, ChatResponse

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return process_question(request.question)