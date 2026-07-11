def result_to_markdown(rows: list[dict]) -> str:
    if not rows:
        return "No rows returned."

    headers = list(rows[0].keys())

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for row in rows:
        lines.append(
            "| " + " | ".join(str(row[h]) for h in headers) + " |"
        )

    return "\n".join(lines)