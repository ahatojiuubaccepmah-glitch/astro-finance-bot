from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import get_main_menu
from keyboards.finance_menu import get_finance_menu
from keyboards.natal_menu import get_natal_menu

router = Router()


# ✅ назад в главное меню
@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer(
        "Главное меню",
        reply_markup=get_main_menu()
    )


# ✅ вход в финансы
@router.message(F.text == "📅 Финансы")
async def open_finance(message: Message):
    await message.answer(
        "Раздел финансов",
        reply_markup=get_finance_menu()
    )


# ✅ вход в натальную карту
@router.message(F.text == "🔮 Натальная карта")
async def open_natal(message: Message):
    await message.answer(
        "Раздел натальной карты",
        reply_markup=get_natal_menu()
    )
