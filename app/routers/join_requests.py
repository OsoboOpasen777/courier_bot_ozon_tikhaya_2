# app/routers/join_requests.py
import logging
from aiogram import Router, F, Bot
from aiogram.types import ChatMemberUpdated, ChatPermissions
from aiogram.enums import ChatMemberStatus
from app.config.settings import settings
from app.services.db import get_user

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

# app/routers/join_requests.py
@router.chat_member()
async def on_member_update(event: ChatMemberUpdated, bot: Bot):
    # если GROUP_ID не задан — просто логируем и выходим
    if not settings.GROUP_ID:
        log.debug("GROUP_ID is not set; got chat_member for %s", event.chat.id)
        return

    if event.chat.id != settings.GROUP_ID:
        # лог поможет понять, не перепутан ли chat.id
        log.debug("Ignoring chat_member: %s (expected %s)", event.chat.id, settings.GROUP_ID)
        return

    old = event.old_chat_member
    new = event.new_chat_member
    log.info("chat_member: %s -> %s for user %s", old.status, new.status, new.user.id)

    if new.status == ChatMemberStatus.MEMBER and old.status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}:
        uid = new.user.id
        user = get_user(uid)
        if user:
            try:
                await bot.restrict_chat_member(settings.GROUP_ID, uid, permissions=FULL)
            except Exception:
                pass
            log.info("Approved member %s (%s) — full permissions", new.user.username, uid)
        else:
            await bot.restrict_chat_member(settings.GROUP_ID, uid, permissions=READONLY)
            try:
                await bot.send_message(
                    uid,
                    "Привет! Доступ в группу только для зарегистрированных.\n"
                    "Напиши боту в личке: /start — пройди короткую регистрацию (ФИО + телефон).",
                )
            except Exception as e:
                log.warning("Cannot DM user %s (%s): %s", new.user.username, uid, e)
            log.info("Restricted unregistered user %s (%s)", new.user.username, uid)

