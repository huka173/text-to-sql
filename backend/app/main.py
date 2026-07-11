from fastapi import FastAPI

from app.services.chat_service import process_question
from app.services.wren_service import execute_sql
from app.services.openai_service import create_chat_completion
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.openai import ChatCompletionRequest

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return process_question(request.question)

@app.post("/v1/chat/completions")
def chat_completions(request: ChatCompletionRequest):
    return create_chat_completion(request)