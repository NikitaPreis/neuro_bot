from sqlalchemy.ext.asyncio import AsyncSession

from bot.interfaces import SQLAlchemyRepository
from bot.models import TGUser


class TGUserRepo(SQLAlchemyRepository):
    """Telegram user repository."""
    model = TGUser

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
