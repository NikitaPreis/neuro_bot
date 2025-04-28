from pydantic import Field
from pydantic_settings import BaseSettings

from bot.settings.configs.database import DBSettings
from bot.settings.configs.giga_chat import GigaChatSettings
from bot.settings.configs.telegram import TelegramSettings


class Settings(BaseSettings):
    """Main settings."""
    db: DBSettings = Field(default_factory=DBSettings)
    telegram: TelegramSettings = Field(default_factory=TelegramSettings)
    giga_chat: GigaChatSettings = Field(default_factory=GigaChatSettings)

    @classmethod
    def load(cls) -> 'Settings':
        return cls()
