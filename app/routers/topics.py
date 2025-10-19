from aiogram.filters import Command
from aiogram.types import Message
from app.services import db import upsert_topic, list_topics

def register(dp):
    dp.message.register(on_forum_topic_created, lambda m: m.forum_topic_created is not None)
    dp.message.register(cmd_where, Command("where"))
    dp.message.register(cmd_topics, Command("topics"))

async def on_forum_topic_created(message: Message):
    tid = message.message_thread_id
    name = message.forum_topic_created.name if message.forum_topic_created else ""
    if tid:
        upsert_topic(chat_id=message.chat.id, thread_id=tid, name=name)
        await message.reply(f"РўРµРјР° СЃРѕР·РґР°РЅР° (thread_id={tid}){' В«'+name+'В»' if name else ''}.")

async def cmd_where(message: Message):
    if message.is_topic_message:
        tid = message.message_thread_id
        topics = list_topics(message.chat.id)
        name = next((t['name'] for t in topics if t['thread_id'] == tid), "")
        await message.answer(f"РЎРµР№С‡Р°СЃ РІС‹ РІ С‚РµРјРµ {tid}{' В«'+name+'В»' if name else ''}.")
    else:
        await message.answer("Р­С‚Рѕ РЅРµ С‚РµРјР°.")

async def cmd_topics(message: Message):
    topics = list_topics(message.chat.id)
    if not topics:
        return await message.answer("РўРµРј РїРѕРєР° РЅРµС‚.")
    lines = [f"вЂў #{t['thread_id']}: {t['name'] or '(Р±РµР· РЅР°Р·РІР°РЅРёСЏ)'}" for t in topics]
    await message.answer("РўРµРјС‹:\n" + "\n".join(lines))

