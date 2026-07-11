import json
from pathlib import Path

MDL_PATH = Path("/app/wren/target/mdl.json")

def build_context() -> str:
    with open(MDL_PATH, encoding="utf-8") as f:
        mdl = json.load(f)

    lines = []

    lines.append("Database schema")
    lines.append("")

    models = mdl.get("models", [])

    for model in models:
        lines.append(f"Table: {model['name']}")

        columns = model.get("columns", [])

        for column in columns:
            column_name = column.get("name")
            column_type = column.get("type", "unknown")

            lines.append(f"  - {column_name} ({column_type})")

        lines.append("")

    relationships = mdl.get("relationships", [])

    if relationships:
        lines.append("Relationships:")

        for rel in relationships:
            lines.append(
                f"  {rel['models'][0]} -> {rel['models'][1]}"
            )

        lines.append("")

    return "\n".join(lines)