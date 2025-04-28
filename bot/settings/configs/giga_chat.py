from bot.settings.configs.base_config import BaseConfig


class GigaChatSettings(BaseConfig):
    """Giga Chat settings."""
    GIGA_CHAT_CLIENT_ID: str = ''
    GIGA_CHAT_AUTH_KEY: str = ''
    GIGA_CHAT_SCOPE: str = 'GIGACHAT_API_PERS'

    GIGA_CHAT_AUTH_URL: str = (
        'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    )
    GIGA_CHAT_REQUEST_URL: str = (
        'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
    )

    GIGA_CHAT_PROMT_MAX_TOKENS: int = 250
