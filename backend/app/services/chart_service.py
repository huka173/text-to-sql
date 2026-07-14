def build_chart(
    result: list[dict],
    chart_type: str,
):

    if chart_type == "none":
        return None

    if not result:
        return None


    columns = list(result[0].keys())


    category = None
    value = None


    for column in columns:

        sample = result[0][column]

        if isinstance(sample, (int, float)):
            value = column

        else:
            category = column


    if category is None or value is None:
        return None


    return {
        "title": {
            "text": f"{value} by {category}"
        },

        "tooltip": {
            "trigger": "axis"
        },

        "xAxis": {
            "type": "category",
            "data": [
                row[category]
                for row in result
            ]
        },

        "yAxis": {
            "type": "value"
        },

        "series": [
            {
                "type": chart_type,
                "data": [
                    row[value]
                    for row in result
                ]
            }
        ]
    }