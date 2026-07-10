import json
import subprocess
import re

WREN_PATH = "/app/wren"

BLOCKED = re.compile(
    r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE)\b",
    re.IGNORECASE,
)

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

    if BLOCKED.search(sql):
        raise RuntimeError("Forbidden SQL operation")

    if not sql.lstrip().upper().startswith("SELECT"):
        raise RuntimeError("Only SELECT queries are allowed")