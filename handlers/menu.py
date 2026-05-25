from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import get_main_menu

router = Router()


@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer(
        "Главное меню",
        reply_markup=get_main_menu()
    )


@router.message(F.text)
async def menu_handler(message: Message):
    text = message.text

    if text == "📅 Финансы":
        await message.answer("Раздел финансов (скоро)")
    elif text == "🔮 Натальная карта":
        await message.answer("Раздел натальной карты (скоро)")