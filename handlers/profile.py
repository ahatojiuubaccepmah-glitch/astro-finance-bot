from aiogram import Router, F
from aiogram.types import Message

from keyboards.profile_menu import get_profile_menu

router = Router()


@router.message(F.text == "👤 Профиль")
async def profile_handler(message: Message):
    await message.answer(
        "📄 Профиль пока пуст",
        reply_markup=get_profile_menu()
    )
