from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_finance_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Календарь")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )