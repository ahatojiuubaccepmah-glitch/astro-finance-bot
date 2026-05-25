from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re

from keyboards.profile_menu import get_profile_menu
from db.database import save_user, get_user, get_city, save_city
from services.geocoder import geocode_city
from services.timezone_service import get_timezone

router = Router()


class ProfileForm(StatesGroup):
    birth_date = State()
    birth_time = State()
    city = State()


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


@router.message(F.text == "👤 Профиль")
async def profile_handler(message: Message):
    user = get_user(message.from_user.id)

    if user:
        await message.answer(
            f"📄 Ваш профиль:\n\n"
            f"📅 Дата: {user['birth_date']}\n"
            f"⏰ Время: {user['birth_time']}\n"
            f"🌍 Город: {user['city']}\n"
            f"📍 Широта: {user['lat']}\n"
            f"📍 Долгота: {user['lon']}\n"
            f"🕒 Таймзона: {user['timezone']}",
            reply_markup=get_profile_menu()
        )
    else:
        await message.answer(
            "📄 Профиль пока пуст",
            reply_markup=get_profile_menu()
        )


@router.message(F.text == "✏️ Редактировать")
async def start_profile_edit(message: Message, state: FSMContext):
    await message.answer("📅 Введите дату рождения\n\nПример: 01.01.2000")
    await state.set_state(ProfileForm.birth_date)


@router.message(ProfileForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    date = message.text.strip()

    if not validate_date(date):
        try:
            date = normalize_date(date)
            if not validate_date(date):
                raise ValueError
        except:
            await message.answer("❌ Неверный формат даты")
            return

    await state.update_data(birth_date=date)

    await message.answer("⏰ Введите время (14:30 или 'не знаю')")
    await state.set_state(ProfileForm.birth_time)


@router.message(ProfileForm.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    time = message.text.strip().lower()

    if time == "не знаю":
        time = "12:00"
    elif not validate_time(time):
        await message.answer("❌ Неверный формат времени")
        return

    await state.update_data(birth_time=time)

    await message.answer("🌍 Введите город")
    await state.set_state(ProfileForm.city)


@router.message(ProfileForm.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()

    if len(city) < 2:
        await message.answer("❌ Введите нормальный город")
        return

    geo = get_city(city)

    if not geo:
        geo = geocode_city(city)

        if not geo:
            await message.answer("❌ Город не найден")
            return

        save_city(city, geo["lat"], geo["lon"])

    timezone = get_timezone(geo["lat"], geo["lon"])

    data = await state.get_data()

    save_user(
        message.from_user.id,
        data["birth_date"],
        data["birth_time"],
        city,
        geo["lat"],
        geo["lon"],
        timezone
    )

    await message.answer(
        f"✅ Профиль сохранён\n\n"
        f"📅 {data['birth_date']}\n"
        f"⏰ {data['birth_time']}\n"
        f"🌍 {city}\n"
        f"📍 {geo['lat']} / {geo['lon']}\n"
        f"🕒 {timezone}",
        reply_markup=get_profile_menu()
    )

    await state.clear()