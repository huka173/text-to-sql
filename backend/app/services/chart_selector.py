def select_chart_type(result):

    prompt = f"""
Choose chart type.

Available:
bar
line
pie
scatter
none

Data:
{result}

Answer only one word.
"""

    response = ollama.generate(prompt)

    return response.strip()