import re
import json
import httpx

MODEL = "qwen2.5-coder:7b"

client = httpx.Client(
    base_url="http://ollama:11434",
    timeout=120,
)

def clean_sql(sql: str) -> str:
    sql = sql.strip()

    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()

def generate_sql(question: str, context: str) -> str:

    prompt = f"""
You are an expert PostgreSQL developer.

Database schema:

{context}

Rules:

- Use ONLY tables from the schema.
- Use ONLY columns from the schema.
- Never invent tables.
- Never invent columns.
- Generate ONE PostgreSQL SELECT query.
- Never use INSERT.
- Never use UPDATE.
- Never use DELETE.
- Never use DROP.
- Never use ALTER.
- Never use TRUNCATE.
- Never use markdown.
- Never explain anything.
- Output ONLY SQL.

- If the question cannot be answered using the schema, return:
SELECT 'Cannot answer using available schema' AS message;
- Never guess missing tables or columns.

Time series rules:
- If the user asks for data by month, week, or year, return a single date/time column.
- Use DATE_TRUNC() for grouping by time periods.
- Do not split dates into separate year and month columns.
- Always ORDER BY the date column.

For cumulative values:
- If data represents cumulative totals and user asks for period values,
calculate the difference between current and previous period.
- Use LAG() window function.

Visualization rules:

- If the user request requires a chart, return exactly TWO columns.
- The first column must be the X-axis.
- The second column must be the numeric Y-axis.
- Do not return separate year and month columns.
- For time series use:

DATE_TRUNC('month', date_column) AS period

instead of:

EXTRACT(YEAR ...)
EXTRACT(MONTH ...)

- Always ORDER BY the X-axis column.

Examples:

Bad:
year | month | count

Good:
period | count

User question:

{question}
"""

    response = client.post(
        "/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0,
        },
    )

    response.raise_for_status()

    data = response.json()

    sql = data.get("response")

    if not sql:
        raise RuntimeError("Ollama returned an empty response.")

    return clean_sql(sql)

def select_chart_type(
    question: str,
    sql: str,
    result: list[dict]
) -> str:

    if not result:
        return "none"

    sample = result[:5]

    columns = []

    for key, value in sample[0].items():
        columns.append(
            {
                "name": key,
                "type": type(value).__name__
            }
        )

    prompt = f"""
        You are a data visualization expert.

        Your task is to choose the BEST chart type.

        Allowed answers:

        bar
        line
        pie
        scatter

        Rules:

        - category + numeric -> bar
        - date/time + numeric -> line
        - percentage/share -> pie
        - two numeric columns -> scatter

        Chart rules:
        - A real date/time column + numeric value should use line chart.
        - Month/year strings representing time should use line chart.
        - Aggregated counts over categories should use bar chart.
        - Distribution of categories should use pie chart.
        - Two numeric metrics should use scatter chart.

        Return ONLY one word.

        User question:

        {question}

        Generated SQL:

        {sql}

        Columns:

        {json.dumps(columns, ensure_ascii=False, indent=2)}

        Sample rows:

        {json.dumps(sample, ensure_ascii=False, indent=2)}
    """

    response = client.post(
        "/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0,
        },
    )

    response.raise_for_status()

    data = response.json()

    chart_type = data["response"].strip().lower()

    allowed = {
        "bar",
        "line",
        "pie",
        "scatter",
        "none",
    }

    if chart_type not in allowed:
        return "bar"

    return chart_type