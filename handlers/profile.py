from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("profile"))
async def profile_handler(message: Message):
    await message.answer("Профиль не заполнен")