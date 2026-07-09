import subprocess
import json

WREN_PATH = "/app/wren"

BLOCKED = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE"
]


def validate_sql(sql: str):
    upper = sql.upper()

    for word in BLOCKED:
        if word in upper:
            raise Exception(
                f"Forbidden SQL operation: {word}"
            )

def execute_sql(sql: str):
    result = subprocess.run(
        [
            "wren",
            "query",
            "--sql",
            sql,
            "--output",
            "json",
        ],
        cwd=WREN_PATH,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    return [
        json.loads(line)
        for line in result.stdout.splitlines()
        if line.strip()
    ]