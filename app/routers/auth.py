# courier_bot/src/handlers/auth.py
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from app.services import db import is_registered, upsert_courier
from ..config import INVITE_LINK
from ..keyboards.inline import join_kb, main_menu_kb
from ..keyboards.reply import main_reply_kb
import html

def register(dp):
    # /start (+ deep-link)
    dp.message.register(cmd_start, CommandStart())

    # Р›СЋР±РѕРµ РїРµСЂРІРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ РІ Р›РЎ в†’ Р°РІС‚Рѕ-РјРµРЅСЋ
    dp.message.register(private_autogreet, F.chat.type == "private", ~F.from_user.is_bot)

    # РљРЅРѕРїРєР° "Р’СЃС‚СѓРїРёС‚СЊ"
    dp.callback_query.register(on_join, F.data == "join")

async def _send_full_menu(message: Message, is_admin: bool = False):
    # 1) inline РјРµРЅСЋ
    await message.answer("Р“Р»Р°РІРЅРѕРµ РјРµРЅСЋ:", reply_markup=main_menu_kb(is_admin=is_admin))
    # 2) reply РјРµРЅСЋ
    await message.answer("Р‘С‹СЃС‚СЂРѕРµ РјРµРЅСЋ РІРєР»СЋС‡РµРЅРѕ.", reply_markup=main_reply_kb())

async def cmd_start(message: Message):
    """
    РџРѕРґРґРµСЂР¶РёРІР°РµС‚ deep-link: /start register
    """
    payload = ""
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) == 2:
        payload = parts[1].strip()

    # РµСЃР»Рё deep-link "register" вЂ” СЃСЂР°Р·Сѓ РїРѕРєР°Р·С‹РІР°РµРј СЂРµРіРёСЃС‚СЂР°С†РёСЋ
    if payload.lower() == "register":
        await message.answer("РќР°Р¶РјРё РєРЅРѕРїРєСѓ, С‡С‚РѕР±С‹ Р·Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°С‚СЊСЃСЏ Рё РїРѕР»СѓС‡РёС‚СЊ СЃСЃС‹Р»РєСѓ РІ РіСЂСѓРїРїСѓ:", reply_markup=join_kb())
        return

    # РѕР±С‹С‡РЅС‹Р№ /start
    await message.answer("РќР°Р¶РјРё РєРЅРѕРїРєСѓ, С‡С‚РѕР±С‹ Р·Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°С‚СЊСЃСЏ Рё РїРѕР»СѓС‡РёС‚СЊ СЃСЃС‹Р»РєСѓ РІ РіСЂСѓРїРїСѓ:", reply_markup=join_kb())

    # РµСЃР»Рё СѓР¶Рµ Р·Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°РЅ вЂ” СЃСЂР°Р·Сѓ РїРѕРєР°Р¶РµРј Рё РјРµРЅСЋ, С‡С‚РѕР±С‹ РЅРµ Р¶РґР°С‚СЊ РєРЅРѕРїРєРё
    if is_registered(message.from_user.id):
        await _send_full_menu(message)

async def private_autogreet(message: Message):
    """
    Р›СЋР±РѕРµ РїРµСЂРІРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ РІ Р›РЎ в†’ РѕС‚РІРµС‚ СЃ РјРµРЅСЋ.
    Р•СЃР»Рё РќР• Р·Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°РЅ вЂ” РїРѕРєР°Р¶РµРј РєРЅРѕРїРєСѓ РІСЃС‚СѓРїР»РµРЅРёСЏ.
    """
    if not is_registered(message.from_user.id):
        await message.answer("РќР°Р¶РјРё РєРЅРѕРїРєСѓ, С‡С‚РѕР±С‹ Р·Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°С‚СЊСЃСЏ Рё РїРѕР»СѓС‡РёС‚СЊ СЃСЃС‹Р»РєСѓ РІ РіСЂСѓРїРїСѓ:", reply_markup=join_kb())
    else:
        await _send_full_menu(message)

async def on_join(call: CallbackQuery):
    uid = call.from_user.id
    full_name = f"{call.from_user.first_name or ''} {call.from_user.last_name or ''}".strip()
    username = call.from_user.username or ""
    if not is_registered(uid):
        upsert_courier(uid, username, full_name)
    await call.message.answer("Р“РѕС‚РѕРІРѕ! РўС‹ Р·Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°РЅ вњ…")
    if INVITE_LINK:
        await call.message.answer(f"РЎСЃС‹Р»РєР° РІ РіСЂСѓРїРїСѓ: {INVITE_LINK}")
    # РїРѕСЃР»Рµ СЂРµРіРёСЃС‚СЂР°С†РёРё СЃСЂР°Р·Сѓ РІС‹РґР°РґРёРј РјРµРЅСЋ
    await _send_full_menu(call.message)
    await call.answer()

