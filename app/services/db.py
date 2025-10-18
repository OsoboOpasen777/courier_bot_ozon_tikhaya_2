
from typing import Optional
from supabase import create_client, Client
from app.config.settings import settings

_client: Optional[Client] = None

def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _client

def get_user(user_id: int) -> dict | None:
    r = get_client().table(settings.COURIERS_TABLE).select("*").eq("user_id", user_id).limit(1).execute()
    return r.data[0] if r.data else None

def upsert_user(*, user_id: int, username: str | None, full_name: str, phone: str, role: str = "courier") -> None:
    payload = {
        "user_id": user_id,
        "username": username or "",
        "full_name": full_name,
        "real_name": full_name,
        "phone": phone,
        "role": role,
    }
    get_client().table(settings.COURIERS_TABLE).upsert(payload, on_conflict="user_id").execute()
