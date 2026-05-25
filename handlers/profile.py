from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re

from keyboards.profile_menu import get_profile_menu
from db.database import save_user, get_user, get_city, save_city

from services.geocoder import geocode_city
from services.timezone_service import get_timezone
from services.time_converter import convert_to_utc
from services.julian import to_julian_date
from services.astro_engine import build_natal_chart

router = Router()


class ProfileForm(StatesGroup):
    birth_date = State()
    birth_time = State()
    city = State()


# ✅ Валидация
def validate_date(date: str) -> bool:
    return bool(re.match(r"^\d{2}\.\d{2}\.\d{4}$", date))


def validate_time(time: str) -> bool:
    return bool(re.match(r"^\d{2}:\d{2}$", time))


def normalize_date(date: str) -> str:
    try:
        d, m, y = date.split(".")
        return f"{int(d):02}.{int(m):02}.{y}"
    except:
        return date


# ✅ ПРОФИЛЬ
@router.message(F.text == "👤 Профиль")
async def profile_handler(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer(
            "📄 Профиль пуст",
            reply_markup=get_profile_menu()
        )
        return

    city_data = get_city(user["city_name"])

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

    # ✅ JD
    jd = to_julian_date(utc_data["datetime"])

    # ✅ Astro Engine (всё в одном месте)
    chart = build_natal_chart(
        utc_data["datetime"],
        city_data["lat"],
        city_data["lon"]
    )

    # ✅ Планеты + дома
    planets_text = "\n".join([
        f"{name}: {data['sign']} — дом {data['house']}"
        for name, data in chart["planets"].items()
    ])

    # ✅ Дома (формат ТЗ)
    houses_text = "\n".join([
        f"{name}: {data['formatted']}"
        for name, data in chart["houses"].items()
    ])

    # ✅ Аспекты
    aspects_text = "\n".join(chart["aspects"]) if chart["aspects"] else "нет"

    await message.answer(
        f"📄 Ваш профиль:\n\n"
        f"📅 Дата: {user['birth_date']}\n"
        f"⏰ Время: {user['birth_time']}\n"
        f"🌍 Город: {user['city_name']}\n"
        f"📍 {city_data['lat']} / {city_data['lon']}\n"
        f"🕒 {city_data['timezone']}\n\n"
        f"🌐 UTC:\n{utc_data['utc_date']} {utc_data['utc_time']}\n\n"
        f"🪐 Julian Date:\n{jd:.5f}\n\n"
        f"📊 Планеты:\n{planets_text}\n\n"
        f"🏠 Дома:\n{houses_text}\n\n"
        f"🔺 Аспекты:\n{aspects_text}",
        reply_markup=get_profile_menu()
    )


# ✅ РЕДАКТИРОВАНИЕ
@router.message(F.text == "✏️ Редактировать")
async def start_profile_edit(message: Message, state: FSMContext):
    await message.answer(
        "📅 Введите дату рождения\n\n"
        "Формат: ДД.ММ.ГГГГ\n"
        "Пример: 01.01.2000"
    )
    await state.set_state(ProfileForm.birth_date)


# ✅ ДАТА
@router.message(ProfileForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    date = message.text.strip()

    if not validate_date(date):
        try:
            date = normalize_date(date)
            if not validate_date(date):
                raise ValueError
        except:
            await message.answer("❌ Неверный формат даты\nВведите: 01.01.2000")
            return

    await state.update_data(birth_date=date)

    await message.answer(
        "⏰ Введите время рождения\n\n"
        "Формат: ЧЧ:ММ\n"
        "Пример: 14:30\n\n"
        "Если не знаете — напишите: не знаю"
    )

    await state.set_state(ProfileForm.birth_time)


# ✅ ВРЕМЯ
@router.message(ProfileForm.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    time = message.text.strip().lower()

    if time == "не знаю":
        time = "12:00"
    elif not validate_time(time):
        await message.answer("❌ Неверный формат времени")
        return

    await state.update_data(birth_time=time)

    await message.answer(
        "🌍 Введите город рождения\n\n"
        "Пример: Москва"
    )

    await state.set_state(ProfileForm.city)


# ✅ ГОРОД
@router.message(ProfileForm.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()

    if len(city) < 2:
        await message.answer("❌ Введите город")
        return

    # ✅ проверка кэша
    city_data = get_city(city)

    if not city_data:
        geo = geocode_city(city)

        if not geo:
            await message.answer("❌ Город не найден")
            return

        timezone = get_timezone(geo["lat"], geo["lon"])

        save_city(city, geo["lat"], geo["lon"], timezone)

        city_data = {
            "lat": geo["lat"],
            "lon": geo["lon"],
            "timezone": timezone
        }

    data = await state.get_data()

    save_user(
        message.from_user.id,
        data["birth_date"],
        data["birth_time"],
        city
    )

    await message.answer(
        "✅ Профиль сохранён",
        reply_markup=get_profile_menu()
    )

    await state.clear()