# courier_bot/src/handlers/health.py
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import F
import sys, platform, aiogram, asyncio, aiohttp
from app.services import db import supabase

def register(dp):
    dp.message.register(cmd_health, Command("health"))
    dp.callback_query.register(cb_health, F.data == "health")

async def _supabase_ok() -> bool:
    try:
        supabase.table("couriers").select("user_id").limit(1).execute()
        return True
    except Exception:
        return False

async def _net_ok() -> bool:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.coingecko.com/api/v3/ping", timeout=5) as r:
                return r.status == 200
    except Exception:
        return False

async def _report_text() -> str:
    s_ok, n_ok = await asyncio.gather(_supabase_ok(), _net_ok())
    return (
        f"рџ©є Health:\n"
        f"вЂў Supabase: {'OK' if s_ok else 'FAIL'}\n"
        f"вЂў Network:  {'OK' if n_ok else 'FAIL'}\n"
        f"вЂў aiogram:  {aiogram.__version__}\n"
        f"вЂў Python:   {sys.version.split()[0]} ({platform.system()})"
    )

async def cmd_health(m: Message):
    await m.answer(await _report_text())

async def cb_health(c: CallbackQuery):
    await c.message.edit_text(await _report_text())
    await c.answer()

