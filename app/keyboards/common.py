
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Взять заказ"), KeyboardButton(text="Мои задания")]],
        resize_keyboard=True
    )
