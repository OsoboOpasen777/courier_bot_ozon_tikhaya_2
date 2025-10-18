
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config.settings import settings
from app.routers import registration, menu, health
from app.utils.logging import setup_logging

async def main():
    setup_logging()
    log = logging.getLogger("bootstrap")

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(health.router)
    dp.include_router(registration.router)
    dp.include_router(menu.router)

    log.info("Bot starting in long-polling mode")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
