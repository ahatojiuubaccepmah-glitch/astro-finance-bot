import asyncio
from aiogram import Bot, Dispatcher

from handlers import start, menu, profile
from handlers import finance
from db.database import create_table   # ✅ добавили импорт

TOKEN = "8788138114:AAHBV2v8ld_KN49gmGMeR0AVNTnF_JywcLM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ подключение handlers
dp.include_router(start.router)
dp.include_router(profile.router)
dp.include_router(menu.router)
dp.include_router(finance.router)

async def main():
    create_table()   # ✅ ВОТ ЗДЕСЬ
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
