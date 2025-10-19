from aiogram.filters import Command
from aiogram import F
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram import Bot
import logging, time
from ..keyboards.inline import main_menu_kb, topics_menu_kb
from ..keyboards.reply import main_reply_kb, remove_kb
from ..config import has_role

log = logging.getLogger(__name__)

# РќРµ СЃРїР°РјРёРј: РїРѕРєР°Р·С‹РІР°РµРј РјРµРЅСЋ РІ РѕРґРЅРѕРј С‡Р°С‚Рµ/С‚СЂРµРґРµ РЅРµ С‡Р°С‰Рµ, С‡РµРј СЂР°Р· РІ 5 РјРёРЅСѓС‚
_SHOWN_KEY_TS: dict[tuple[int, int], float] = {}
_COOLDOWN = 300  # СЃРµРє

def _key_for(msg: Message) -> tuple[int, int]:
    """РљР»СЋС‡ 'С‡Р°С‚ + С‚СЂРµРґ' (РґР»СЏ РѕР±С‹С‡РЅРѕРіРѕ С‡Р°С‚Р° thread_id=0)."""
    return (msg.chat.id, msg.message_thread_id or 0)

async def _show_both_menus(where, is_admin: bool):
    # where: РѕР±СЉРµРєС‚ Message РёР»Рё Bot+chat_id вЂ” РЅРѕ Р·РґРµСЃСЊ РјС‹ РёСЃРїРѕР»СЊР·СѓРµРј message
    msg: Message = where
    # 1) inline
    await msg.answer("Р“Р»Р°РІРЅРѕРµ РјРµРЅСЋ:", reply_markup=main_menu_kb(is_admin=is_admin))
    # 2) reply (persistent)
    await msg.answer("Р‘С‹СЃС‚СЂРѕРµ РјРµРЅСЋ РІРєР»СЋС‡РµРЅРѕ.", reply_markup=main_reply_kb())

def register(dp):
    # 0) РљРѕРіРґР° Р‘РћРўРђ РґРѕР±Р°РІРёР»Рё/РїРѕРІС‹СЃРёР»Рё РІ С‡Р°С‚Рµ вЂ” СЃСЂР°Р·Сѓ РІРєР»СЋС‡Р°РµРј РјРµРЅСЋ РґР»СЏ РІСЃРµС…
    dp.my_chat_member.register(on_bot_joined_or_promoted)

    # 1) РЇРІРЅС‹Р№ РІС…РѕРґ РІ РјРµРЅСЋ
    dp.message.register(cmd_menu, Command("menu"))
    dp.callback_query.register(on_menu, F.data.startswith("menu:"))

    # 2) Р РµРїР»Р°Р№-РєРЅРѕРїРєРё
    dp.message.register(on_reply_buttons, F.text.in_([
        "рџ“‹ РњРµРЅСЋ", "рџ§µ РўРµРјС‹", "рџ©є РџСЂРѕРІРµСЂРєР°", "вќЊ РЎРєСЂС‹С‚СЊ РјРµРЅСЋ"
    ]))

    # 3) РђРІС‚Рѕ-Р°РєС‚РёРІР°С†РёСЏ РјРµРЅСЋ РїСЂРё Р›Р®Р‘РћРњ СЃРѕРѕР±С‰РµРЅРёРё РІ РіСЂСѓРїРїРµ/СЃСѓРїРµСЂРіСЂСѓРїРїРµ (РЅРµ С‚РѕР»СЊРєРѕ РІ С‚РµРјР°С…)
    dp.message.register(auto_menu_any_group, F.chat.type.in_({"group", "supergroup"}), ~F.from_user.is_bot)

    # 4) РћСЃС‚Р°Р»СЊРЅРѕРµ
    dp.message.register(cmd_ping, Command("ping"))
    dp.callback_query.register(cb_fallback)
    dp.message.register(msg_fallback)

# в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ handlers в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ

async def on_bot_joined_or_promoted(upd: ChatMemberUpdated, bot: Bot):
    """
    РЎСЂР°Р±Р°С‚С‹РІР°РµС‚, РєРѕРіРґР° Р±РѕС‚Р° РґРѕР±Р°РІРёР»Рё РІ С‡Р°С‚ РёР»Рё РїРѕРІС‹СЃРёР»Рё.
    РџРѕРєР°Р·С‹РІР°РµРј РІСЃРµРј РѕР±С‰РµРµ РјРµРЅСЋ (inline + reply) РІ РєРѕСЂРЅРµРІРѕРј С‡Р°С‚Рµ.
    """
    new_status = upd.new_chat_member.status
    if new_status in {"administrator", "member"}:
        try:
            # РїРѕРєР°Р·С‹РІР°РµРј РѕР±Р° РјРµРЅСЋ РѕРґРёРЅ СЂР°Р· РїСЂРё РїРѕРґРєР»СЋС‡РµРЅРёРё
            await bot.send_message(upd.chat.id, "Р‘РѕС‚ РїРѕРґРєР»СЋС‡С‘РЅ. РќР°РІРёРіР°С†РёСЏ:",
                                   reply_markup=main_menu_kb(is_admin=False))
            await bot.send_message(upd.chat.id, "Р‘С‹СЃС‚СЂРѕРµ РјРµРЅСЋ РІРєР»СЋС‡РµРЅРѕ.",
                                   reply_markup=main_reply_kb())
        except Exception as e:
            log.warning(f"cannot send welcome menus to chat {upd.chat.id}: {e}")

async def cmd_menu(message: Message):
    is_admin = has_role(message.from_user.id, "admin")
    await _show_both_menus(message, is_admin)

async def on_menu(call: CallbackQuery):
    action = call.data.split(":", 1)[1]
    if action == "topics":
        await call.message.edit_text("РњРµРЅСЋ С‚РµРј:", reply_markup=topics_menu_kb())
    elif action == "admin":
        if not has_role(call.from_user.id, "admin"):
            await call.answer("РќРµС‚ РґРѕСЃС‚СѓРїР°", show_alert=True); return
        await call.message.edit_text("РђРґРјРёРЅ-РїР°РЅРµР»СЊ (Р±РѕР»РІР°РЅРєР°). Р’РµСЂРЅРёСЃСЊ РІ /menu.",
                                     reply_markup=main_menu_kb(is_admin=True))
    await call.answer()

async def on_reply_buttons(message: Message):
    txt = (message.text or "").strip()
    if txt == "рџ“‹ РњРµРЅСЋ":
        is_admin = has_role(message.from_user.id, "admin")
        await message.answer("Р“Р»Р°РІРЅРѕРµ РјРµРЅСЋ:", reply_markup=main_menu_kb(is_admin=is_admin))
    elif txt == "рџ§µ РўРµРјС‹":
        await message.answer("РњРµРЅСЋ С‚РµРј:", reply_markup=topics_menu_kb())
    elif txt == "рџ©є РџСЂРѕРІРµСЂРєР°":
        # РљРЅРѕРїРєР° Р·Р°РїСѓСЃРєР°РµС‚ inline-С…РµРЅРґР»РµСЂ (health.py). РџРѕРґСЃРєР°Р¶РµРј РЅР°Р¶Р°С‚СЊ С‚Р°Рј.
        await message.answer("РќР°Р¶РјРёС‚Рµ В«рџ©є РџСЂРѕРІРµСЂРєР°В» РІ РёРЅР»Р°Р№РЅ-РјРµРЅСЋ РІС‹С€Рµ.", reply_markup=main_menu_kb())
    elif txt == "вќЊ РЎРєСЂС‹С‚СЊ РјРµРЅСЋ":
        await message.answer("РњРµРЅСЋ СЃРєСЂС‹С‚Рѕ. Р’РµСЂРЅСѓС‚СЊ вЂ” /menu.", reply_markup=remove_kb())

async def auto_menu_any_group(message: Message):
    """
    РђРІС‚РѕРјР°С‚РёС‡РµСЃРєРѕРµ РІРєР»СЋС‡РµРЅРёРµ РјРµРЅСЋ РІ Р›Р®Р‘РћРњ СЃРѕРѕР±С‰РµРЅРёРё РіСЂСѓРїРїС‹/СЃСѓРїРµСЂРіСЂСѓРїРїС‹.
    Р Р°Р±РѕС‚Р°РµС‚ Рё РІ РєРѕСЂРЅРµ С‡Р°С‚Р°, Рё РІ С‚РµРјР°С… (СЂР°Р·РЅС‹Рµ РєР»СЋС‡Рё).
    """
    key = _key_for(message)
    now = time.time()
    if now - _SHOWN_KEY_TS.get(key, 0) < _COOLDOWN:
        return
    _SHOWN_KEY_TS[key] = now

    is_admin = has_role(message.from_user.id, "admin")
    await _show_both_menus(message, is_admin)

async def cmd_ping(message: Message):
    await message.answer("pong вњ…")

async def cb_fallback(c: CallbackQuery):
    await c.answer("рџ¤” РљРЅРѕРїРєР° РЅРµ СЂР°СЃРїРѕР·РЅР°РЅР°", show_alert=False)

async def msg_fallback(m: Message):
    if m.chat.type == "private":
        await m.answer("РћС‚РєСЂРѕР№ /menu РґР»СЏ РґРµР№СЃС‚РІРёР№.")

