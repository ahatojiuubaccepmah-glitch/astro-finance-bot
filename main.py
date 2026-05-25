
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.main_menu import get_main_menu

TOKEN = "8788138114:AAHnpHY8zzZy_ENvSWb9KwjchtVyJfH_7QM"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать 🚀",
        reply_markup=get_main_menu()
    )


@dp.message()
async def menu_handler(message: Message):
    text = message.text

    if text == "📅 Финансы":
        await message.answer("Раздел финансов открыт")
    elif text == "🔮 Натальная карта":
        await message.answer("Раздел натальной карты")
    elif text == "👤 Профиль":
        await message.answer("Твой профиль")
    else:
        await message.answer("Не понимаю команду")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())