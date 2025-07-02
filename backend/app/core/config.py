import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL", "sqlite:///./data/transcriptions.db")
    audio_dir: str = os.getenv("AUDIO_DIR", "temp")

    model_config = SettingsConfigDict(validate_default=False)


settings = Settings()


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.propagate = False

# Prevent duplicate handlers in reload scenarios
if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)
