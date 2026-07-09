import httpx

OLLAMA_URL = "http://ollama:11434"
MODEL = "qwen2.5-coder:7b"

def generate_sql(question: str):

    prompt = f"""
Ты генератор SQL.

У тебя есть база данных сотрудников.

Таблицы:

employees:
- id
- full_name
- department_id
- hire_date

departments:
- id
- name

salaries:
- id
- employee_id
- amount

Связи:

employees.department_id = departments.id

salaries.employee_id = employees.id


Напиши только SQL запрос.
Без объяснений.
Без markdown.

Вопрос:
{question}
"""


    response = httpx.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]