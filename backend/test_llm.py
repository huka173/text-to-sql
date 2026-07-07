from llm import generate_sql


system_prompt = """
You are an expert PostgreSQL developer.

Return ONLY SQL.
Do not explain.
Do not use markdown.
"""

question = """
Database schema:

departments(id, name)

employees(
    id,
    full_name,
    department_id,
    hire_date
)

Question:
Покажи всех сотрудников отдела разработки.
"""

result = generate_sql(
    prompt=question,
    system=system_prompt
)

print(result)