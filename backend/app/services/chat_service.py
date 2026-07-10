from app.services.prompt_service import build_context
from app.services.ollama_service import generate_sql
from app.services.wren_service import (
    validate_sql,
    execute_sql,
)

def process_question(question: str):
    context = build_context()

    sql = generate_sql(question, context)

    validate_sql(sql)

    result = execute_sql(sql)

    return {
        "context": context,
        "sql": sql,
        "result": result,
    }