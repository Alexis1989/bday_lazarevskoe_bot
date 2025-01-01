from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def kb_names(names):
    keyboard = InlineKeyboardBuilder()

    for name in names:
        keyboard.row(InlineKeyboardButton(
            text=f"{name}", callback_data=f"name_{name.replace(" ", "_")}"))

    return keyboard.as_markup()
