import re
from aiogram.filters import Command
from aiogram.types import Message
from ..http_client import get_http_session

def register(dp):
    dp.message.register(cmd_btc, Command("btc"))
    dp.message.register(cmd_title, Command("title"))

async def cmd_btc(message: Message):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    session = await get_http_session()
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return await message.answer(f"API СЃС‚Р°С‚СѓСЃ {resp.status}")
        data = await resp.json()
        price = data.get("bitcoin", {}).get("usd")
        await message.answer(f"в‚ї Bitcoin: ${price:,}" if price else "РќРµ СѓРґР°Р»РѕСЃСЊ РїРѕР»СѓС‡РёС‚СЊ С†РµРЅСѓ.")

async def cmd_title(message: Message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Р¤РѕСЂРјР°С‚: /title https://example.com")
    url = parts[1].strip()
    if not re.match(r"^https?://", url, re.I):
        return await message.answer("РЈРєР°Р¶Рё РїРѕР»РЅС‹Р№ URL.")
    session = await get_http_session()
    async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
        if resp.status != 200:
            return await message.answer(f"РЎС‚Р°С‚СѓСЃ {resp.status}")
        html = await resp.text()
    m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I|re.S)
    await message.answer(f"В«{re.sub(r'\\s+', ' ', m.group(1)).strip()}В»" if m else "РўРµРі <title> РЅРµ РЅР°Р№РґРµРЅ.")

