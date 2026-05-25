from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
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