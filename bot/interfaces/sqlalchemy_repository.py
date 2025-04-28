from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.exceptions import DataBaseException
from bot.interfaces import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    """SQLAlchemy abstract repository."""
    model = None

    def __init__(self, db_session: AsyncSession):
        self.db_session: AsyncSession = db_session

    async def get(self, model_schema: BaseModel):
        """
        Get model obj from database.
        """
        query = select(self.model).where(self.model.id == model_schema.id)
        try:
            async with self.db_session as session:
                return (await session.execute(query)).scalar_one_or_none()
        except SQLAlchemyError:
            raise DataBaseException

    async def create(self, model_schema: BaseModel) -> int:
        """
        Add model obj to database.
        """
        data = model_schema.model_dump()

        stmt = insert(self.model).values(
            data
        ).returning(self.model.id)

        try:
            async with self.db_session as session:
                model_id = (await session.execute(stmt)).scalar_one_or_none()
                await session.commit()
                return model_id
        except SQLAlchemyError:
            raise DataBaseException

    async def exists(self, model_schema: BaseModel):
        """
        Check obj exists.
        """
        query = select(self.model.id).where(self.model.id == model_schema.id)
        try:
            async with self.db_session as session:
                return (await session.execute(query)).scalar_one_or_none()
        except SQLAlchemyError:
            raise DataBaseException
