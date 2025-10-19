from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from app.services.db import get_user
from app.keyboards.common import courier_menu, supervisor_menu, owner_menu

router = Router(name="menu")

def _pick_menu(role: str):
    if role == "owner":
        return owner_menu()
    if role == "supervisor":
        return supervisor_menu()
    return courier_menu()

@router.message(Command("menu"))
async def show_menu(message: Message):
    u = get_user(message.from_user.id)
    if not u:
        await message.reply("Сначала пройди регистрацию в личке: /start")
        return
    await message.reply("Меню:", reply_markup=_pick_menu(u.get("role", "courier")))

# Примеры обработчиков кнопок
@router.callback_query(F.data == "m:profile")
async def cb_profile(call: CallbackQuery):
    u = get_user(call.from_user.id)
    if not u:
        await call.message.answer("Профиль не найден. Пройди регистрацию: /start")
    else:
        text = (
            "👤 Профиль\n"
            f"ФИО: {u.get('full_name')}\n"
            f"Телефон: {u.get('phone')}\n"
            f"Роль: {u.get('role')}"
        )
        await call.message.answer(text)
    await call.answer()

@router.callback_query(F.data == "m:help")
async def cb_help(call: CallbackQuery):
    await call.message.answer("Памятка курьера:\n— Правило 1\n— Правило 2\n— Правило 3")
    await call.answer()

@router.callback_query(F.data == "m:contact")
async def cb_contact(call: CallbackQuery):
    await call.message.answer("Связь с супервайзером: напишите @supervisor_username")
    await call.answer()
