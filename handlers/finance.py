from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime

from keyboards.main_menu import get_main_menu
from keyboards.finance_menu import get_finance_menu
from db.database import get_user, get_city

from services.time_converter import convert_to_utc
from services.astro_engine import build_natal_chart
from services.calendar_builder import build_month_calendar
from services.calendar_png import create_calendar_png

from aiogram.types import FSInputFile

router = Router()


# ✅ Вход в финансы
@router.message(F.text == "📅 Финансы")
async def finance_menu(message: Message):
    await message.answer(
        "📊 Финансовый раздел",
        reply_markup=get_finance_menu()
    )


# ✅ Назад
@router.message(F.text == "⬅️ Назад")
async def back_to_menu(message: Message):
    await message.answer(
        "Главное меню",
        reply_markup=get_main_menu()
    )


# ✅ Календарь
@router.message(F.text == "📅 Календарь")
async def finance_calendar(message: Message):
    print("clicked calendar")

    user = get_user(message.from_user.id)

    if not user:
        await message.answer("❌ Сначала заполните профиль")
        return

    city_Ы

data = get_city(user["city_name"])

    if not city_data:
        await message.answer("❌ Ошибка города")
        return

    # ✅ UTC
    utc_data = convert_to_utc(
        user["birth_date"],
        user["birth_time"],
        city_data["timezone"]
    )

    if not utc_data or "error" in utc_data:
        await message.answer("❌ Ошибка времени")
        return

    # ✅ Натальная карта
    chart = build_natal_chart(
        utc_data["datetime"],
        city_data["lat"],
        city_data["lon"]
    )

    # ✅ текущий месяц
    now = datetime.now()

    # ✅ строим календарь
    calendar_data = build_month_calendar(
        chart,
        now.year,
        now.month
    )

    # ✅ создаём PNG
    path = create_calendar_png(
        calendar_data,
        now.year,
        now.month
    )

    # ✅ отправляем файл
    await message.answer_photo(
        FSInputFile(path),
        caption="📅 Финансовый календарь"
    )