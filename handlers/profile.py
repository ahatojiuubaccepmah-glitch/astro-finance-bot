from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re

from keyboards.profile_menu import get_profile_menu

router = Router()


# ✅ FSM
class ProfileForm(StatesGroup):
    birth_date = State()
    birth_time = State()
    city = State()


# ✅ Валидация даты
def validate_date(date: str) -> bool:
    pattern = r"^\d{2}\.\d{2}\.\d{4}$"
    return bool(re.match(pattern, date))


# ✅ Валидация времени
def validate_time(time: str) -> bool:
    pattern = r"^\d{2}:\d{2}$"
    return bool(re.match(pattern, time))


# ✅ Нормализация даты (1.1.2000 → 01.01.2000)
def normalize_date(date: str) -> str:
    parts = date.split(".")
    if len(parts) == 3:
        d, m, y = parts
        return f"{int(d):02}.{int(m):02}.{y}"
    return date


# ✅ Профиль
@router.message(F.text == "👤 Профиль")
async def profile_handler(message: Message):
    await message.answer(
        "📄 Профиль пока пуст",
        reply_markup=get_profile_menu()
    )


# ✅ Старт редактирования
@router.message(F.text == "✏️ Редактировать")
async def start_profile_edit(message: Message, state: FSMContext):
    await message.answer(
        "📅 Введите дату рождения\n\nПример: 01.01.2000"
    )
    await state.set_state(ProfileForm.birth_date)


# ✅ Ввод даты
@router.message(ProfileForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    date = message.text.strip()

    if not validate_date(date):
        # пробуем нормализовать
        try:
            date = normalize_date(date)
            if not validate_date(date):
                raise ValueError
        except:
            await message.answer(
                "❌ Неверный формат даты\n\nВведите так: 01.01.2000"
            )
            return

    await state.update_data(birth_date=date)

    await message.answer(
        "⏰ Введите время рождения\n\nПример: 14:30\n\n"
        "Если не знаете — напишите: не знаю"
    )

    await state.set_state(ProfileForm.birth_time)


# ✅ Ввод времени
@router.message(ProfileForm.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    time = message.text.strip().lower()

    if time == "не знаю":
        time = "12:00"
    else:
        if not validate_time(time):
            await message.answer(
                "❌ Неверный формат времени\n\nВведите так: 14:30\n"
                "Или напишите: не знаю"
            )
            return

    await state.update_data(birth_time=time)

    await message.answer(
        "🌍 Введите город рождения\n\nПример: Москва"
    )

    await state.set_state(ProfileForm.city)


# ✅ Ввод города и завершение
@router.message(ProfileForm.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()

    if len(city) < 2:
        await message.answer("❌ Введите нормальное название города")
        return

    await state.update_data(city=city)

    data = await state.get_data()

    await message.answer(
        f"✅ Профиль сохранён\n\n"
        f"📅 Дата: {data['birth_date']}\n"
        f"⏰ Время: {data['birth_time']}\n"
        f"🌍 Город: {data['city']}",
        reply_markup=get_profile_menu()
    )

    await state.clear()