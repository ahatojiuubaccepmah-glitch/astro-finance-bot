from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.profile_menu import get_profile_menu

router = Router()


# ✅ FSM состояния
class ProfileForm(StatesGroup):
    birth_date = State()
    birth_time = State()
    city = State()


# ✅ кнопка "Профиль"
@router.message(F.text == "👤 Профиль")
async def profile_handler(message: Message):
    await message.answer(
        "📄 Профиль пока пуст",
        reply_markup=get_profile_menu()
    )


# ✅ кнопка "Редактировать"
@router.message(F.text == "✏️ Редактировать")
async def start_profile_edit(message: Message, state: FSMContext):
    await message.answer(
        "Введите дату рождения\n\nПример: 01.01.2000"
    )
    await state.set_state(ProfileForm.birth_date)


# ✅ ввод даты
@router.message(ProfileForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)

    await message.answer(
        "Введите время рождения\n\nПример: 14:30"
    )

    await state.set_state(ProfileForm.birth_time)


# ✅ ввод времени
@router.message(ProfileForm.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)

    await message.answer(
        "Введите город рождения\n\nПример: Москва"
    )

    await state.set_state(ProfileForm.city)


# ✅ ввод города и завершение
@router.message(ProfileForm.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    data = await state.get_data()

    await message.answer(
        f"✅ Профиль сохранён\n\n"
        f"📅 Дата: {data['birth_date']}\n"
        f"⏰ Время: {data['birth_time']}\n"
        f"🌍 Город: {data['city']}"
    )

    await state.clear()
