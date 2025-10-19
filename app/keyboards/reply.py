# courier_bot/src/keyboards/reply.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def main_reply_kb() -> ReplyKeyboardMarkup:
    # persistent-РєР»Р°РІРёР°С‚СѓСЂР° РІРЅРёР·Сѓ СЌРєСЂР°РЅР°
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="рџ“‹ РњРµРЅСЋ"), KeyboardButton(text="рџ§µ РўРµРјС‹")],
            [KeyboardButton(text="рџ©є РџСЂРѕРІРµСЂРєР°"), KeyboardButton(text="вќЊ РЎРєСЂС‹С‚СЊ РјРµРЅСЋ")],
        ],
        is_persistent=True,   # Р·Р°РєСЂРµРїР»СЏРµРј
        resize_keyboard=True,
        input_field_placeholder="Р’С‹Р±РµСЂРёС‚Рµ РґРµР№СЃС‚РІРёРµвЂ¦",
    )

def remove_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()

