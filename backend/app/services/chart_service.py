def build_chart(result: list[dict]):

    if not result:
        return None

    columns = list(result[0].keys())

    if len(columns) != 2:
        return None

    x = columns[0]
    y = columns[1]

    if not isinstance(result[0][y], (int, float)):
        return None

    return {
        "type": "bar",
        "title": f"{y} by {x}",
        "x": x,
        "y": y,
        "data": result,
    }