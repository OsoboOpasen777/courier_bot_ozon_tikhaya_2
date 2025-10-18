
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Меню скоро будет расширено: 'Взять заказ', 'Мои задания', 'Отчитаться о доставке'.")
