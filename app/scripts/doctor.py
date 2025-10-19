# scripts/doctor.py
import asyncio, os, sys, textwrap
from typing import List
from dotenv import load_dotenv, find_dotenv

def fail(msg): print("❌", msg); sys.exit(1)
def ok(msg):   print("✅", msg)

def check_env():
    load_dotenv(find_dotenv())
    need = ["BOT_TOKEN","SUPABASE_URL","SUPABASE_KEY","COURIERS_TABLE"]
    missing = [k for k in need if not os.getenv(k)]
    if missing: fail(f".env: нет переменных {missing}")
    ok(".env: переменные на месте")

async def check_telegram():
    from aiogram import Bot
    bot = Bot(token=os.getenv("BOT_TOKEN",""))
    me = await bot.get_me()
    ok(f"Telegram: @{me.username} доступен")

def check_supabase():
    from supabase import create_client
    url, key = os.getenv("SUPABASE_URL",""), os.getenv("SUPABASE_KEY","")
    sb = create_client(url, key)
    tables: List[str] = ["couriers","orders","assignments","delivery_events","order_status_history"]
    misses=[]
    for t in tables:
        try:
            sb.table(t).select("*").limit(1).execute()
        except Exception:
            misses.append(t)
    if misses:
        fail(f"Supabase: нет таблиц {misses}. Выполни SQL из папки migrations/")
    ok("Supabase: все базовые таблицы на месте")

def main():
    print("== courier_bot DOCTOR ==")
    # 1) git (опциональная проверка)
    os.system("git status --porcelain > .gitstatus.tmp")
    changed = open(".gitstatus.tmp","r",encoding="utf-8").read().strip()
    os.remove(".gitstatus.tmp")
    if changed:
        print("⚠️  Git: есть незафиксированные изменения"); print(changed)
    else:
        ok("Git: рабочее дерево чистое")

    # 2) env
    check_env()

    # 3) Supabase
    check_supabase()

    # 4) Telegram
    asyncio.run(check_telegram())

    print("🎉 Всё выглядит синхронно. Можно редактировать и коммитить.")

if __name__ == "__main__":
    main()
