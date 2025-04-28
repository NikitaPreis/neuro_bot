"""Module dependencies."""
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from bot.clients.giga_chat import GigaChatClient
from bot.database import get_db_session
from bot.repositories import MessageRepo, TGUserRepo
from bot.services.gpt import GPTService
from bot.settings import Settings


def get_settings() -> Settings:
    """Get settings/config."""
    return Settings.load()


async def get_async_client() -> httpx.AsyncClient:
    """Get async client."""
    return httpx.AsyncClient()


async def get_giga_chat_client() -> GigaChatClient:
    """Get giga chat client."""
    client: httpx.AsyncClient = await get_async_client()
    settings: Settings = get_settings()
    return GigaChatClient(
        async_client=client,
        settings=settings
    )


async def get_tg_user_repo() -> TGUserRepo:
    """Get telegram user repository."""
    db_session: AsyncSession = await get_db_session()
    return TGUserRepo(db_session=db_session)


async def get_message_repo() -> MessageRepo:
    """Get messages repository."""
    db_session: AsyncSession = await get_db_session()
    return MessageRepo(db_session=db_session)


async def get_gpt_service() -> GPTService:
    """Get GPT service."""
    giga_chat = await get_giga_chat_client()
    tg_user_repo = await get_tg_user_repo()
    message_repo = await get_message_repo()
    return GPTService(
        gpt_client=giga_chat,
        message_repo=message_repo,
        user_repo=tg_user_repo
    )
