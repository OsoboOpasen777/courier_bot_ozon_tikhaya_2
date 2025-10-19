import logging
from aiogram import Router, F, Bot
from aiogram.types import ChatMemberUpdated, ChatPermissions, Message
from aiogram.enums import ChatMemberStatus
from app.config.settings import settings
from app.services.db import get_user
from app.keyboards.common import courier_menu, supervisor_menu, owner_menu

router = Router(name="group_access")
log = logging.getLogger("group-access")

READONLY = ChatPermissions(can_send_messages=False)
FULL = ChatPermissions(
    can_send_messages=True,
    can_send_audios=True,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
)

def _is_target_group(chat_id: int) -> bool:
    if not settings.GROUP_ID:
        log.debug("GROUP_ID is not set; skip chat %s", chat_id)
        return False
    if chat_id != settings.GROUP_ID:
        log.debug("Ignore chat %s (expected %s)", chat_id, settings.GROUP_ID)
        return False
    return True

def _pick_menu(role: str):
    if role == "owner":
        return owner_menu()
    if role == "supervisor":
        return supervisor_menu()
    return courier_menu()

async def _welcome_registered(bot: Bot, chat_id: int, user_id: int):
    u = get_user(user_id)
    role = u.get("role", "courier") if u else "courier"
    kb = _pick_menu(role)
    try:
        await bot.restrict_chat_member(chat_id, user_id, permissions=FULL)
    except Exception:
        pass
    # Показываем меню прямо в группе:
    await bot.send_message(chat_id, "Добро пожаловать! Твоё меню ниже 👇", reply_markup=kb)

async def _tell_to_register(bot: Bot, chat_id: int, user_id: int):
    me = await bot.get_me()
    deep = f"https://t.me/{me.username}?start=reg"
    await bot.restrict_chat_member(chat_id, user_id, permissions=READONLY)
    await bot.send_message(
        chat_id,
        f"Доступ к сообщению закрыт до регистрации.\n"
        f"Перейди в личку с ботом и пройди регистрацию: {deep}",
    )

# Вариант 1: смена статуса участника
@router.chat_member()
async def on_member_update(event: ChatMemberUpdated, bot: Bot):
    if not _is_target_group(event.chat.id):
        return
    old, new = event.old_chat_member, event.new_chat_member
    log.info("chat_member: %s -> %s for user %s", old.status, new.status, new.user.id)

    if new.status == ChatMemberStatus.MEMBER and old.status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}:
        if get_user(new.user.id):
            await _welcome_registered(bot, event.chat.id, new.user.id)
        else:
            await _tell_to_register(bot, event.chat.id, new.user.id)

# Вариант 2: message.new_chat_members (часто приходит именно он)
@router.message(F.new_chat_members)
async def on_new_members(message: Message, bot: Bot):
    if not _is_target_group(message.chat.id):
        return
    ids = [u.id for u in message.new_chat_members]
    log.info("new_chat_members: %s", ids)
    for uid in ids:
        if get_user(uid):
            await _welcome_registered(bot, message.chat.id, uid)
        else:
            await _tell_to_register(bot, message.chat.id, uid)
