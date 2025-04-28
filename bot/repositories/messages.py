from sqlalchemy.ext.asyncio import AsyncSession

from bot.interfaces import SQLAlchemyRepository
from bot.models import Message


class MessageRepo(SQLAlchemyRepository):
    """Message repository."""
    model = Message

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
