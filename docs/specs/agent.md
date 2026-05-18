# Спецификация агента-оркестратора (кратко)

## Класс: `LLMTravelAgent` (`agent/llm.py`)

### Метод: `async def process_message(system_prompt, user_prompt) -> str`

**Алгоритм:**
1. Создать `messages` = [system, user]
2. Запросить Mistral (`mistral-large-latest`, `temperature=0.7`, `tools=TOOLS`)
3. Цикл до 5 итераций:
   - Если нет `tool_calls` → выход
   - Добавить ответ ассистента в `messages`
   - Выполнить каждый `tool_call` (сейчас только `search_internet`)
   - Добавить результат как `role="tool"`
   - Снова запросить Mistral
4. Вернуть `assistant_message.content` (или строку-заглушку)

### Stop conditions
- Нет вызовов инструментов
- Достигнуто 5 итераций

### Недостатки (важно!)
- История **не сохраняется** между разными вызовами `process_message`
- Нет обработки исключений API
- Нет retry при ошибке инструмента
