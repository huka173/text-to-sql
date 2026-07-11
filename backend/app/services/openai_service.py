import time

from app.services.chat_service import process_question
from app.utils.formatter import result_to_markdown

def create_chat_completion(request):
    start = time.time()

    question = request.messages[-1].content

    answer = process_question(question)

    sql = answer["sql"]
    rows = result_to_markdown(answer["result"])

    content = f"""## SQL

```sql
{sql}
```

## Result:

{rows}
"""

    return {
        "id": f"chatcmpl-{int(start)}",
        "object": "chat.completion",
        "created": int(start),
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop",
            }
        ],
    }