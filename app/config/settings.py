
import os, re
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def _ids(env: str) -> set[int]:
    s = os.getenv(env, "")
    return {int(x) for x in re.findall(r"\d+", s)} if s else set()

class Settings(BaseModel):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    COURIERS_TABLE: str = os.getenv("COURIERS_TABLE", "couriers")

    OWNER_IDS: set[int] = _ids("OWNER_IDS")
    ADMIN_IDS: set[int] = _ids("ADMIN_IDS")
    SUPERVISOR_IDS: set[int] = _ids("SUPERVISOR_IDS")

settings = Settings()
