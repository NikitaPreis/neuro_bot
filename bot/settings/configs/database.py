from bot.settings.configs.base_config import BaseConfig


class DBSettings(BaseConfig):
    """Database settings."""

    # DB connection credentials (ORM).
    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_PASSWORD: str = 'mysecretpassword'
    DB_USER: str = 'postgres'
    DB_NAME: str = 'neuro_bot'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432

    @property
    def db_url(self):
        return (f'{self.DB_DRIVER}://{self.DB_USER}:'
                f'{self.DB_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}')
