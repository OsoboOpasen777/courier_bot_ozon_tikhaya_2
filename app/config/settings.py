from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    BOT_TOKEN: str
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # имена переменных
    COURIERS_TABLE: str = "couriers"
    TOPICS_TABLE: str = "topics"

    # опциональные
    GROUP_ID: Optional[int] = None          
    INVITE_LINK: Optional[str] = None
    OWNER_ID: Optional[int] = None

    model_config = {"env_file": ".env", "env_prefix": ""}

settings = Settings()

