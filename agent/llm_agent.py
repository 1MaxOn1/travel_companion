import json
from openai import OpenAI
from config.settings import MISTRAL_API_KEY
from agent.tools import search_internet

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "Поиск в интернете. Возвращает заголовки, ссылки и сниппеты. Используй для поиска билетов, отелей, достопримечательностей, ресторанов, погоды, визовых требований и любой другой актуальной информации.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"}
                },
                "required": ["query"]
            }
        }
    }
]

class LLMTravelAgent:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.mistral.ai/v1",
            api_key=MISTRAL_API_KEY,
        )

    async def process_message(self, system_prompt: str, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = self.client.chat.completions.create(
            model="mistral-large-latest",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.7
        )
        assistant_message = response.choices[0].message

        for _ in range(5):
            if not assistant_message.tool_calls:
                break
            messages.append(assistant_message)
            for tool_call in assistant_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                if func_name == "search_internet":
                    result = search_internet(func_args["query"])
                else:
                    result = {"error": f"Unknown function {func_name}"}
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })
            response = self.client.chat.completions.create(
                model="mistral-large-latest",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.7
            )
            assistant_message = response.choices[0].message

        return assistant_message.content or "Извините, не удалось сформировать ответ."