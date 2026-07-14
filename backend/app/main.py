from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import json
import asyncio

from app.services.chat_service import process_question
from app.services.wren_service import execute_sql
from app.services.openai_service import create_chat_completion
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.openai import ChatCompletionRequest

app = FastAPI()

async def stream_chat_completion(request):
    response = create_chat_completion(request)

    content = response["choices"][0]["message"]["content"]

    chunk = {
        "id": response["id"],
        "object": "chat.completion.chunk",
        "created": response["created"],
        "model": response["model"],
        "choices": [
            {
                "index": 0,
                "delta": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": None,
            }
        ],
    }

    yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

    await asyncio.sleep(0.01)

    finish = {
        "id": response["id"],
        "object": "chat.completion.chunk",
        "created": response["created"],
        "model": response["model"],
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "stop",
            }
        ],
    }

    yield f"data: {json.dumps(finish)}\n\n"

    yield "data: [DONE]\n\n"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()

    completion_request = ChatCompletionRequest(**body)

    print("stream =", completion_request.stream)

    if completion_request.stream:
        return StreamingResponse(
            stream_chat_completion(completion_request),
            media_type="text/event-stream"
        )

    return create_chat_completion(completion_request)

@app.get("/v1/models")
def models():
    return {
        "object": "list",
        "data": [
            {
                "id": "text-to-sql",
                "object": "model",
                "owned_by": "local"
            }
        ]
    }