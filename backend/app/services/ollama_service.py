import re

import httpx

MODEL = "qwen2.5-coder:7b"

client = httpx.Client(
    base_url="http://ollama:11434",
    timeout=120,
)

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
- Never use TRUNCATE.
- Never use markdown.
- Never explain anything.
- Output ONLY SQL.
- If the question cannot be answered using the schema, return:
SELECT 'Cannot answer using available schema' AS message;
- Never guess missing tables or columns.

User question:

{question}
"""

    response = client.post(
        "/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0,
        },
    )

    response.raise_for_status()

    data = response.json()

    sql = data.get("response")

    if not sql:
        raise RuntimeError("Ollama returned an empty response.")

    return clean_sql(sql)