from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.database import Base


class Message(Base):
    """
    Table for message sessions: one message per telegram user and GPT.
    """
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True
    )

    # User text message (promt).
    request_text: Mapped[str]

    # GPT response.
    response_text: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey('tg_users.id'), nullable=False
    )
