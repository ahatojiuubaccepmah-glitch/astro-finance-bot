import asyncio
from aiogram import Bot, Dispatcher

from handlers import start, menu, profile
from db.database import create_table   # ✅ добавили импорт

TOKEN = "8788138114:AAHnpHY8zzZy_ENvSWb9KwjchtVyJfH_7QM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ подключение handlers
dp.include_router(start.router)
dp.include_router(profile.router)
dp.include_router(menu.router)


async def main():
    create_table()   # ✅ ВОТ ЗДЕСЬ
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
