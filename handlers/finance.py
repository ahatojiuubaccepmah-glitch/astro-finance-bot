from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from datetime import datetime

from keyboards.main_menu import get_main_menu
from keyboards.finance_menu import get_finance_menu

from db.database import get_user, get_city

from services.time_converter import convert_to_utc
from services.astro_engine import build_natal_chart
from services.calendar_builder import build_month_calendar
from services.calendar_png import create_calendar_png

router = Router()


# ✅ DEBUG — ловит ВСЁ (временно!)
@router.message()
async def debug_all(message: Message):
    print("DEBUG TEXT:", message.text)


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


# ✅ Календарь (будем править после DEBUG)
@router.message(F.text == "📅 Календарь")
async def finance_calendar(message: Message):
    print("CLICKED CALENDAR")

    try:
        user = get_user(message.from_user.id)

        if not user:
            await message.answer("❌ Сначала заполните профиль")
            return

        city_data = get_city(user["city_name"])

        if not city_data:
            await message.answer("❌ Ошибка города")
            return

        utc_data = convert_to_utc(
            user["birth_date"],
            user["birth_time"],
            city_data["timezone"]
        )

        if not utc_data or "error" in utc_data:
            await message.answer("❌ Ошибка времени")
            return

        chart = build_natal_chart(
            utc_data["datetime"],
            city_data["lat"],
            city_data["lon"]
        )

        now = datetime.now()

        calendar_data = build_month_calendar(
            chart,
            now.year,
            now.month
        )

        path = create_calendar_png(
            calendar_data,
            now.year,
            now.month
        )

        await message.answer_photo(
            FSInputFile(path),
            caption="📅 Финансовый календарь"
        )

    except Exception as e:
        print("ERROR:", e)
        await message.answer("❌ Ошибка при расчёте календаря")