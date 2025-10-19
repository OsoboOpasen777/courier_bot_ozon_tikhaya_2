import os, re
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

found = find_dotenv(".env", raise_error_if_not_found=False)
if found: load_dotenv(found)
here_env = Path(__file__).with_name(".env")
if here_env.exists(): load_dotenv(here_env)

BOT_TOKEN      = (os.getenv("BOT_TOKEN") or "").strip()
SUPABASE_URL   = (os.getenv("SUPABASE_URL") or "").strip()
SUPABASE_KEY   = (os.getenv("SUPABASE_KEY") or "").strip()
COURIERS_TABLE = (os.getenv("COURIERS_TABLE") or os.getenv("TABLE_NAME") or "couriers").strip()
TOPICS_TABLE   = (os.getenv("TOPICS_TABLE") or "topics").strip()
INVITE_LINK    = (os.getenv("INVITE_LINK") or "").strip()
LOG_LEVEL      = (os.getenv("LOG_LEVEL") or "INFO").upper()

def _ids(envname: str) -> set[int]:
    s = os.getenv(envname, "")
    return {int(x) for x in re.findall(r"\d+", s)} if s else set()

OWNER_IDS      = _ids("OWNER_IDS")
ADMIN_IDS      = _ids("ADMIN_IDS")
SUPERVISOR_IDS = _ids("SUPERVISOR_IDS")

def has_role(user_id: int, need: str = "supervisor") -> bool:
    """РџСЂР°РІР°: owner вЉѓ admin вЉѓ supervisor."""
    if need == "owner":
        return user_id in OWNER_IDS
    if need == "admin":
        return user_id in OWNER_IDS or user_id in ADMIN_IDS
    return (user_id in OWNER_IDS) or (user_id in ADMIN_IDS) or (user_id in SUPERVISOR_IDS)

