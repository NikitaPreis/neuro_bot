from pydantic import BaseModel


class TGUserSchema(BaseModel):
    """Telegram user schema."""
    id: int
    username: str | None
