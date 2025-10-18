
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.services.db import get_user, upsert_user
from app.keyboards.common import main_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = get_user(message.from_user.id)
    if user:
        await message.answer("Вы уже зарегистрированы. Добро пожаловать!", reply_markup=main_kb())
        return
    await message.answer("Привет! Отправь своё ФИО и телефон через запятую: \nНапример: Иванов Иван, +7 999 123-45-67")

@router.message(F.text.regexp(r".+,\s*\+?\d[\d\s\-\(\)]{7,16}\d$"))
async def handle_registration(message: Message):
    try:
        full_name, phone = [x.strip() for x in message.text.split(",", 1)]
    except Exception:
        return await message.answer("Формат: ФИО, телефон. Попробуй ещё раз.")
    upsert_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=full_name,
        phone=phone,
    )
    await message.answer("Готово! Вы зарегистрированы.", reply_markup=main_kb())
