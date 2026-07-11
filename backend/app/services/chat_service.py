import time

from app.utils.logger import logger
from app.services.prompt_service import build_context
from app.services.ollama_service import generate_sql
from app.services.wren_service import (
    validate_sql,
    execute_sql,
)

def process_question(question: str):
    start = time.perf_counter()

    try:
        context = build_context()

        sql = generate_sql(question, context)

        validate_sql(sql)

        result = execute_sql(sql)

        elapsed = time.perf_counter() - start

        sql_log = sql.replace("\n", " ")

        if len(sql_log) > 300:
            sql_log = sql_log[:300] + "..."

        logger.info(
            "status=SUCCESS | time=%.2fs | rows=%d | question=%r | sql=%r",
            elapsed,
            len(result),
            question,
            sql_log,
        )

        return {
            "sql": sql,
            "result": result,
        }

    except Exception as e:
        elapsed = time.perf_counter() - start

        logger.error(
            "status=ERROR | time=%.2fs | question=%r | error=%r",
            elapsed,
            question,
            str(e),
        )

        raise