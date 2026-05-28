import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import start, menu, profile, finance
from db.database import create_table


# ✅ загружаем .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# ✅ проверка (очень важно)
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")


bot = Bot(token=TOKEN)
dp = Dispatcher()


# ✅ подключение роутеров
dp.include_router(finance.router)
dp.include_router(start.router)
dp.include_router(profile.router)
dp.include_router(menu.router)


async def main():
    create_table()
    await dp.start_polling(bot)


# ✅ точка входа (исправлено)
if __name__ == "__main__":
    asyncio.run(main())