from fastapi import FastAPI

from app.services.chat_service import process_question
from app.services.wren_service import execute_sql
from app.schemas.chat import ChatRequest, ChatResponse

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/test-wren")
def test_wren():

    sql = """
    SELECT
        e.full_name,
        s.amount
    FROM employees e
    JOIN salaries s
        ON e.id = s.employee_id
    LIMIT 5
    """

    result = execute_sql(sql)

    return {
        "result": result
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return process_question(request.question)