import httpx

from config import OLLAMA_URL, OLLAMA_MODEL

def clean_sql(sql: str) -> str:
    sql = sql.strip()

    if sql.startswith("```sql"):
        sql = sql.removeprefix("```sql")

    if sql.startswith("```"):
        sql = sql.removeprefix("```")

    if sql.endswith("```"):
        sql = sql.removesuffix("```")

    return sql.strip()

def generate_sql(prompt: str, system: str) -> str:
    response = httpx.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "system": system,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return clean_sql(data["response"])