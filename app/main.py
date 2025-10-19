import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config.settings import settings
from app.routers import registration, join_requests, menu
from app.utils.logging import setup_logging


async def main():
    setup_logging()
    log = logging.getLogger("bootstrap")

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры
    dp.include_router(registration.router)
    dp.include_router(join_requests.router)
    dp.include_router(menu.router)

    log.info("Routers loaded: %s", [registration.router.name, join_requests.router.name])

    await bot.delete_webhook(drop_pending_updates=True)
    allowed = dp.resolve_used_update_types()
    log.info("Allowed updates: %s", allowed)
    log.info("Bot is starting…")
    await dp.start_polling(bot, allowed_updates=allowed)


if __name__ == "__main__":
    asyncio.run(main())
