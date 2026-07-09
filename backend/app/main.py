from fastapi import FastAPI
from app.services.wren_service import execute_sql
from app.services.ollama_service import generate_sql

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

@app.post("/chat")
def chat(question: str):

    sql = generate_sql(question)
    validate_sql(sql)
    result = execute_sql(sql)

    return {
        "sql": sql,
        "result": result
    }