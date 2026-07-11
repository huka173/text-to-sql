import json
import subprocess
import sqlglot
from sqlglot import expressions as exp

WREN_PATH = "/app/wren"

def run_wren(*args: str) -> str:
    result = subprocess.run(
        ["wren", *args],
        cwd=WREN_PATH,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()

def fetch_context(question: str) -> str:
    return run_wren(
        "memory",
        "fetch",
        "--query",
        question,
    )

def execute_sql(sql: str):
    output = run_wren(
        "query",
        "--sql",
        sql,
        "--output",
        "json",
    )

    return [
        json.loads(line)
        for line in output.splitlines()
        if line.strip()
    ]

def validate_sql(sql: str):
    try:
        tree = sqlglot.parse_one(sql, dialect="postgres")
    except Exception:
        raise RuntimeError("Invalid SQL")

    if not isinstance(tree, exp.Select):
        raise RuntimeError("Only SELECT queries are allowed")