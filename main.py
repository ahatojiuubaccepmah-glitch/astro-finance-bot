import asyncio
from aiogram import Bot, Dispatcher
from handlers import profile
from handlers import start, menu

TOKEN = "8788138114:AAHnpHY8zzZy_ENvSWb9KwjchtVyJfH_7QM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ подключаем роутеры
dp.include_router(start.router)
dp.include_router(menu.router)
dp.include_router(profile.router)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())