from datetime import datetime, date

def is_timestamp(value):

    if isinstance(value, (int, float)):
        # milliseconds unix timestamp
        return value > 100000000000

    return False

def build_chart(
    result: list[dict],
    chart_type: str,
):

    if chart_type == "none":
        return None

    if not result:
        return None

    columns = list(result[0].keys())

    numeric_columns = []
    string_columns = []
    timestamp_columns = []


    for column in columns:
        value = result[0][column]

        if is_timestamp(value):
            timestamp_columns.append(column)
        elif isinstance(value, (int, float)):
            numeric_columns.append(column)
        elif isinstance(value, str):
            string_columns.append(column)

    if chart_type == "scatter":
        if len(numeric_columns) < 2:
            return None

        x_column = numeric_columns[0]
        y_column = numeric_columns[1]

        return {
            "title": {
                "text": f"{y_column} vs {x_column}"
            },

            "tooltip": {
                "trigger": "item"
            },

            "xAxis": {
                "type": "value"
            },

            "yAxis": {
                "type": "value"
            },

            "series": [
                {
                    "type": "scatter",

                    "data": [
                        [
                            row[x_column],
                            row[y_column]
                        ]
                        for row in result
                    ]
                }
            ]
        }

    if chart_type == "pie":
        if len(string_columns) == 0:
            return None

        if len(numeric_columns) == 0:
            return None

        name_column = string_columns[0]
        value_column = numeric_columns[0]

        return {
            "title": {
                "text": f"{value_column} distribution"
            },

            "tooltip": {
                "trigger": "item"
            },

            "series": [
                {
                    "type": "pie",

                    "radius": "50%",

                    "data": [
                        {
                            "name": row[name_column],
                            "value": row[value_column]
                        }

                        for row in result
                    ]
                }
            ]
        }

    x_column = None
    y_column = None

    for column in columns:
        value = result[0][column]

        if is_timestamp(value):

            x_column = column

        elif isinstance(value, (int, float)):
            y_column = column

        elif isinstance(value, str):
            x_column = column

    if x_column is None or y_column is None:
        return None

    if is_timestamp(result[0][x_column]):
        return {
            "title": {
                "text": f"{y_column} by {x_column}"
            },


            "tooltip": {
                "trigger": "axis"
            },


            "xAxis": {
                "type": "time"
            },


            "yAxis": {
                "type": "value"
            },


            "series": [
                {
                    "type": "line",

                    "data": [
                        [
                            row[x_column],
                            row[y_column]
                        ]

                        for row in result
                    ]
                }
            ]
        }

    return {
        "title": {
            "text": f"{y_column} by {x_column}"
        },

        "tooltip": {
            "trigger": "axis"
        },

        "xAxis": {
            "type": "category",

            "data": [
                row[x_column]
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
                    row[y_column]
                    for row in result
                ]
            }
        ]
    }