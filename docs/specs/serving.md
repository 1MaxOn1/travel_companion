# Спецификация сервиса (serving)

## Точка входа
- Бот запускается через `bot.py` (используется `aiogram`)
- Переменные окружения:
  - `BOT_TOKEN` — токен Telegram бота
  - `MISTRAL_API_KEY` — ключ Mistral AI

## Конфигурация
Файл `config/settings.py` (в коде не показан, предполагается):
```python
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
