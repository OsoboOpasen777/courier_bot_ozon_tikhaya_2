# courier_bot/src/keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def join_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="рџџў Р’СЃС‚СѓРїРёС‚СЊ", callback_data="join")
    return kb.as_markup()

def main_menu_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="рџ§µ РўРµРјС‹", callback_data="menu:topics")
    kb.button(text="рџ©є РџСЂРѕРІРµСЂРєР°", callback_data="health")
    if is_admin:
        kb.button(text="рџ›  РђРґРјРёРЅ-РїР°РЅРµР»СЊ", callback_data="menu:admin")
    kb.adjust(2, 1)
    return kb.as_markup()

def topics_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="рџ“ѓ РЎРїРёСЃРѕРє С‚РµРј", callback_data="topics:list")
    kb.button(text="вћ• РЎРѕР·РґР°С‚СЊ С‚РµРјСѓ", callback_data="topics:create")
    kb.button(text="рџ“Ќ Р“РґРµ СЏ?", callback_data="topics:where")
    kb.adjust(2, 1)
    return kb.as_markup()

def topic_select_kb(topics: list[dict]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for t in topics[:30]:
        name = t.get("name") or f"РўРµРјР° #{t.get('thread_id')}"
        kb.button(text=f"рџ§µ {name}", callback_data=f"noop")
    kb.adjust(1)
    return kb.as_markup()

