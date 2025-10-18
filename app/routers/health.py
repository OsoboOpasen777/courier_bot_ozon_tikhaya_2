
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("health"))
async def cmd_health(message: Message):
    await message.answer("OK")
