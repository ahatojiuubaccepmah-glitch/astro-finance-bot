from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_natal_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🪐 Рассчитать карту")],
            [KeyboardButton(text="📊 Аспекты")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )