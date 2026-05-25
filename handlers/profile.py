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

router = Router()


class ProfileForm(StatesGroup):
    birth_date = State()
    birth_time = State()
    city = State()


# ✅ валидация
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


# ✅ просмотр профиля
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

    utc_data = convert_to_utc(
        user["birth_date"],
        user["birth_time"],
        city_data["timezone"]
    )

    jd = to_julian_date(utc_data["datetime"])

    await message.answer(
        f"📄 Ваш профиль:\n\n"
        f"📅 Дата: {user['birth_date']}\n"
        f"⏰ Время: {user['birth_time']}\n"
        f"🌍 Город: {user['city_name']}\n"
        f"📍 {city_data['lat']} / {city_data['lon']}\n"
        f"🕒 {city_data['timezone']}\n\n"
        f"🌐 UTC:\n"
        f"{utc_data['utc_date']} {utc_data['utc_time']}",
        reply_markup=get_profile_menu()
    )


# ✅ старт
@router.message(F.text == "✏️ Редактировать")
async def start_profile_edit(message: Message, state: FSMContext):
    await message.answer("📅 Введите дату рождения")
    await state.set_state(ProfileForm.birth_date)


# ✅ дата
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

    await message.answer("⏰ Введите время")
    await state.set_state(ProfileForm.birth_time)


# ✅ время
@router.message(ProfileForm.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    time = message.text.strip().lower()

    if time == "не знаю":
        time = "12:00"
    elif not validate_time(time):
        await message.answer("❌ Время неверно")
        return

    await state.update_data(birth_time=time)

    await message.answer("🌍 Введите город")
    await state.set_state(ProfileForm.city)


# ✅ город (главная логика)
@router.message(ProfileForm.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()

    if len(city) < 2:
        await message.answer("❌ Введите город")
        return

    # ✅ проверяем кэш
    city_data = get_city(city)

    if not city_data:
        geo = geocode_city(city)

        if not geo:
            await message.answer("❌ Город не найден")
            return

        timezone = get_timezone(geo["lat"], geo["lon"])

        # ✅ сохраняем в cities
        save_city(city, geo["lat"], geo["lon"], timezone)

        city_data = {
            "lat": geo["lat"],
            "lon": geo["lon"],
            "timezone": timezone
        }

    data = await state.get_data()

    # ✅ сохраняем пользователя (только ссылку)
    save_user(
        message.from_user.id,
        data["birth_date"],
        data["birth_time"],
        city
    )

    utc_data = convert_to_utc(
        data["birth_date"],
        data["birth_time"],
        city_data["timezone"]
    )

    jd = to_julian_date(utc_data["datetime"])

    await message.answer(
        f"✅ Профиль сохранён\n\n"
        f"📅 {data['birth_date']}\n"
        f"⏰ {data['birth_time']}\n"
        f"🌍 {city}\n"
        f"🕒 {city_data['timezone']}\n"
        f"🌐 {utc_data['utc_time']}",
	f"🪐 Julian Date:\n{jd:.5f}",
        reply_markup=get_profile_menu()
    )

    await state.clear()