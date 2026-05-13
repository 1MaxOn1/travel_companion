import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
USE_LLM = bool(MISTRAL_API_KEY)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trips.db")