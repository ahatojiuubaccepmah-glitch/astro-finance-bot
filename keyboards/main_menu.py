from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Финансы")],
            [KeyboardButton(text="🔮 Натальная карта")],
            [KeyboardButton(text="👤 Профиль")]
        ],
        resize_keyboard=True
    )


def get_finance_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Календарь")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )