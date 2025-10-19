# -*- coding: utf-8 -*-
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ForceReply

from app.config.settings import settings
from app.keyboards.common import join_keyboard, courier_menu, supervisor_menu, owner_menu
from app.services.db import get_user, upsert_user
from app.utils.validators import NAME_RE, PHONE_RE

router = Router(name="registration")

def _pick_menu(role: str):
    if role == "owner":
        return owner_menu()
    if role == "supervisor":
        return supervisor_menu()
    return courier_menu()

class Reg(StatesGroup):
    waiting_full_name = State()
    waiting_phone = State()

@router.message(CommandStart(), F.chat.type == "private")
async def start(message: Message, state: FSMContext):
    await state.clear()
    u = get_user(message.from_user.id)
    if u:
        await message.answer("Ты уже зарегистрирован. Открой меню:", reply_markup=_pick_menu(u.get("role", "courier")))
        return

    await message.answer(
        "Привет! Для регистрации введи **Фамилию и Имя** одной строкой\nнапример: `Иванов Иван`",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Reg.waiting_full_name)

@router.message(Reg.waiting_full_name, F.chat.type == "private")
async def reg_full_name(message: Message, state: FSMContext):
    full_name = (message.text or "").strip()
    if not NAME_RE.match(full_name):
        await message.answer(
            "Формат не распознан. Пример: `Иванов Иван` (допустимо отчество и дефис). Попробуй ещё раз.",
            parse_mode="Markdown",
            reply_markup=ForceReply(selective=True),
        )
        return
    await state.update_data(full_name=full_name)
    await message.answer(
        "Теперь пришли номер телефона в формате `+7 999 123-45-67`.",
        parse_mode="Markdown",
        reply_markup=ForceReply(selective=True),
    )
    await state.set_state(Reg.waiting_phone)

@router.message(Reg.waiting_phone, F.chat.type == "private")
async def reg_phone(message: Message, state: FSMContext, bot: Bot):
    phone = (message.text or "").strip()
    if not PHONE_RE.match(phone):
        await message.answer(
            "Не похоже на номер. Пример: `+7 999 123-45-67`. Попробуй ещё раз.",
            parse_mode="Markdown",
            reply_markup=ForceReply(selective=True),
        )
        return
    data = await state.get_data()
    full_name = data["full_name"]
    role = "owner" if (settings.OWNER_ID and message.from_user.id == settings.OWNER_ID) else "courier"
    upsert_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=full_name,
        phone=phone,
        role=role,
    )
    await state.clear()
    await message.answer("Готово! Регистрация завершена. Открой меню:", reply_markup=_pick_menu(role))

# /menu в личке
@router.message(Command(commands=["menu"]), F.chat.type == "private")
async def cmd_menu(message: Message):
    u = get_user(message.from_user.id)
    if not u:
        await message.answer("Сначала пройди регистрацию: /start")
        return
    await message.answer("Меню:", reply_markup=_pick_menu(u.get("role", "courier")))

# Кнопка «Вступить» (в личке) — просто подсказка
@router.callback_query(F.data == "join")
async def on_join_click(call: CallbackQuery, bot: Bot):
    me = await bot.get_me()
    await call.message.answer(f"Зайди в группу по ссылке и потом /menu будет доступно.\nЕсли нужно, вот ссылка на бота: https://t.me/{me.username}")
    await call.answer()

# /start и /menu, если нажали в группе — отправим дип-линк
@router.message(CommandStart(), F.chat.type.in_({"group", "supergroup"}))
async def start_in_group(message: Message, bot: Bot):
    me = await bot.get_me()
    await message.reply(f"Регистрация и меню — в личке с ботом: https://t.me/{me.username}?start=reg")

@router.message(Command(commands=["menu"]), F.chat.type.in_({"group", "supergroup"}))
async def menu_in_group_link(message: Message, bot: Bot):
    me = await bot.get_me()
    await message.reply(f"Открой меню в личке: https://t.me/{me.username}?start=menu")
