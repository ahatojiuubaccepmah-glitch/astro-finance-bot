from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from datetime import datetime

from keyboards.main_menu import get_main_menu

from db.database import get_user, get_city

from services.time_converter import convert_to_utc
from services.astro_engine import build_natal_chart
from services.calendar_builder import build_month_calendar
from services.calendar_png import create_calendar_png

router = Router()


# ✅ Назад
@router.message(F.text == "⬅️ Назад")
async def back_to_menu(message: Message):
    await message.answer(
        "Главное меню",
        reply_markup=get_main_menu()
    )


# ✅ DEBUG КАЛЕНДАРЯ
@router.message(F.text == "Календарь")
async def finance_calendar(message: Message):
    print("STEP 0: handler triggered")
    await message.answer("STEP 0 ✅ Кнопка нажата")

    try:
        # ✅ user
        print("STEP 1: get_user")
        user = get_user(message.from_user.id)

        if not user:
            await message.answer("STEP 1 ❌ нет пользователя")
            return

        await message.answer(f"STEP 1 ✅ user найден: {user['city_name']}")

        # ✅ city
        print("STEP 2: get_city")
        city_data = get_city(user["city_name"])

        if not city_data:
            await message.answer("STEP 2 ❌ нет города")
            return

        await message.answer(
            f"STEP 2 ✅ city: {city_data['lat']}, {city_data['lon']}"
        )

        # ✅ UTC
        print("STEP 3: convert_to_utc")
        utc_data = convert_to_utc(
            user["birth_date"],
            user["birth_time"],
            city_data["timezone"]
        )

        if not utc_data or "error" in utc_data:
            await message.answer("STEP 3 ❌ ошибка времени")
            return

        await message.answer("STEP 3 ✅ UTC рассчитан")

        # ✅ chart
        print("STEP 4: build_natal_chart")
        chart = build_natal_chart(
            utc_data["datetime"],
            city_data["lat"],
            city_data["lon"]
        )

        await message.answer("STEP 4 ✅ натальная карта")

        # ✅ calendar
        print("STEP 5: calendar builder")
        now = datetime.now()

        calendar_data = build_month_calendar(
            chart,
            now.year,
            now.month
        )

        await message.answer("STEP 5 ✅ календарь построен")

        # ✅ PNG
        print("STEP 6: render PNG")
        path = create_calendar_png(
            calendar_data,
            now.year,
            now.month
        )

        await message.answer("STEP 6 ✅ PNG создан")

        # ✅ send
        print("STEP 7: send")
        await message.answer_photo(
            FSInputFile(path),
            caption="📅 Финансовый календарь"
        )

        await message.answer("✅ ГОТОВО")

    except Exception as e:
        print("ERROR:", e)
        await message.answer(f"❌ ОШИБКА: {e}")