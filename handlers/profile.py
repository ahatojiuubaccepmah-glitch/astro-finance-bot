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


# ✅ Валидация
def validate_date(date: str) -> bool:
    pattern = r"^\d{2}\.\d{2}\.\d{4}$"
    return bool(re.match(pattern, date))


def validate_time(time: str) -> bool:
    pattern = r"^\d{2}:\d{2}$"
    return bool(re.match(pattern, time))


def normalize_date(date: str) -> str:
    try:
        d, m, y = date.split(".")
        return f"{int(d):02}.{int(m):02}.{y}"
    except:
        return date


# ✅ ПРОФИЛЬ (Теперь с проверкой)
@router.message(F.text == "👤 Профиль")
async def profile_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if data:
        await message.answer(
            f"📄 Ваш профиль:\n\n"
            f"📅 Дата: {data.get('birth_date')}\n"
            f"⏰ Время: {data.get('birth_time')}\n"
            f"🌍 Город: {data.get('city')}",
            reply_markup=get_profile_menu()
        )
    else:
        await message.answer(
            "📄 Профиль пока пуст",
            reply_markup=get_profile_menu()
        )


# ✅ старт редактирования
@router.message(F.text == "✏️ Редактировать")
async def start_profile_edit(message: Message, state: FSMContext):
    await message.answer(
        "📅 Введите дату рождения\n\nПример: 01.01.2000"
    )
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
            await message.answer(
                "❌ Неверный формат даты\n\nВведите так: 01.01.2000"
            )
            return

    await state.update_data(birth_date=date)

    await message.answer(
        "⏰ Введите время\n\nПример: 14:30\n\nили напишите: не знаю"
    )

    await state.set_state(ProfileForm.birth_time)


# ✅ время
@router.message(ProfileForm.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    time = message.text.strip().lower()

    if time == "не знаю":
        time = "12:00"
    else:
        if not validate_time(time):
            await message.answer(
                "❌ Неверный формат времени\n\nВведите так: 14:30"
            )
            return

    await state.update_data(birth_time=time)

    await message.answer(
        "🌍 Введите город рождения\n\nПример: Москва"
    )

    await state.set_state(ProfileForm.city)


# ✅ город + финал
@router.message(ProfileForm.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()

    if len(city) < 2:
        await message.answer("❌ Введите нормальный город")
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

    # ❗ НЕ очищаем state → данные остаются