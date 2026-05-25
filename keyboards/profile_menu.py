from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_profile_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✏️ Редактировать")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )
