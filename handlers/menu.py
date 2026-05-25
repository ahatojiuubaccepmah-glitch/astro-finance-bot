from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.main_menu import get_main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать 🚀",
        reply_markup=get_main_menu()
    )
``