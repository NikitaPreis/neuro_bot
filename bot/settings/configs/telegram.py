from bot.settings.configs.base_config import BaseConfig


class TelegramSettings(BaseConfig):
    """Telegram bot settings."""
    BOT_API_TOKEN: str = ''
