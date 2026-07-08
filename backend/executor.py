from database import get_connection


ALLOWED_STATEMENTS = ("SELECT", "WITH")

def is_safe_query(query: str) -> bool:
    query = query.strip().upper()

    return query.startswith(ALLOWED_STATEMENTS)

def execute_sql(query: str) -> dict:
    query = query.strip()

    upper_query = query.upper()

    if not is_safe_query(query):
        raise ValueError("Only SELECT queries are allowed.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

            columns = [desc.name for desc in cur.description]

            rows = cur.fetchall()

    return {
        "columns": columns,
        "rows": rows
    }