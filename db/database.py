import aiosqlite
import json
from config.settings import DATABASE_URL

DB_PATH = DATABASE_URL.replace("sqlite:///", "")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                params TEXT,
                selected_country TEXT,
                plan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def save_trip(user_id: int, params: dict, country: str, plan: dict):
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO trips (user_id, params, selected_country, plan) VALUES (?, ?, ?, ?)",
            (user_id, json.dumps(params, ensure_ascii=False), country, json.dumps(plan, ensure_ascii=False))
        )
        await db.commit()