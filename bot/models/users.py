from sqlalchemy.orm import Mapped, mapped_column

from bot.database.database import Base


class TGUser(Base):
    """Table for telegram users."""
    __tablename__ = 'tg_users'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True
    )
    username: Mapped[str | None] = mapped_column(
        nullable=True, unique=True
    )
