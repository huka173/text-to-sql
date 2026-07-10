import httpx
import re

OLLAMA_URL = "http://ollama:11434"
MODEL = "qwen2.5-coder:7b"

def clean_sql(sql: str) -> str:
    sql = sql.strip()

    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)

    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()

def generate_sql(question: str, context: str) -> str:

    prompt = f"""
You are an expert PostgreSQL developer.

Database schema:

{context}

Rules:

- Use ONLY tables from the schema.
- Use ONLY columns from the schema.
- Never invent tables.
- Never invent columns.
- Generate ONE PostgreSQL SELECT query.
- Never use INSERT.
- Never use UPDATE.
- Never use DELETE.
- Never use DROP.
- Never use ALTER.
- Never use markdown.
- Never explain anything.
- Output ONLY SQL.

User question:

{question}
"""

    response = httpx.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        },
        timeout=120,
    )

    response.raise_for_status()

    sql = response.json()["response"]

    return clean_sql(sql)