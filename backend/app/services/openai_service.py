import time
import json

from app.services.chat_service import process_question
from app.utils.formatter import result_to_markdown
from app.services.chart_service import build_chart

def create_chat_completion(request):
    start = time.time()

    question = request.messages[-1].content

    answer = process_question(question)

    sql = answer["sql"]
    rows = result_to_markdown(answer["result"])
    chart = build_chart(answer["result"])

    content = f"""## SQL

```sql
{sql}
```

## Result:

{rows}
"""
    if chart:
        chart_json = json.dumps(
            chart,
            ensure_ascii=False,
            indent=2
        )

        content += "\n\n```chart\n"
        content += chart_json
        content += "\n```\n"

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