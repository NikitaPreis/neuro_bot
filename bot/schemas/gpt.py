"""Schemas/DTO for using GPT client."""

from pydantic import BaseModel, Field


class PromtSchema(BaseModel):
    """GPT promt schema."""
    text: str = Field(max_length=500, min_length=1)


class PromtContextSchema(BaseModel):
    """Promt and context schema."""
    context: list[PromtSchema]
    promt: PromtSchema


class GPTResponseSchema(BaseModel):
    """GPT response schema."""
    response_text: str


class GigaChatAccessTokenSchema(BaseModel):
    """Giga Chat access token schema."""
    access_token: str
    expires_at: float


class GPTMessageSessionSchema(BaseModel):
    """
    GPT message session includes data from user request and GPT response.
    """
    request_text: str
    response_text: str
    user_id: int
