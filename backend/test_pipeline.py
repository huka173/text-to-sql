from prompt_builder import build_system_prompt
from llm import generate_sql
from executor import execute_sql


system_prompt = build_system_prompt()

question = input("Введите запрос: ")

sql = generate_sql(question, system_prompt)

print("\nSQL:")
print(sql)

result = execute_sql(sql)

print("\nRESULT:")
print(result)