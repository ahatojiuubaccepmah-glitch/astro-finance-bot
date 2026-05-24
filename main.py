pimport asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = "8788138114:AAHnpHY8zzZy_ENvSWb9KwjchtVyJfH_7QM"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Бот запущен 🚀")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
