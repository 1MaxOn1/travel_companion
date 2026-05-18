# Спецификация инструментов

## Единственный инструмент: `search_internet`
- **Файл:** `agent/tools.py`
- **Функция:** `search_internet(query: str) -> dict`
- **Описание для LLM:** Поиск билетов, отелей, достопримечательностей, погоды и т.д.

## Формат вызова (через Mistral tools)
```json
{
  "name": "search_internet",
  "arguments": {"query": "Париж отели 2026"}
}
