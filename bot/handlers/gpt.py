"""
Handlers for work with GPT.
"""
import logging

from aiogram import F, Router
from aiogram.types import Message

from bot.dependencies import get_gpt_service
from bot.exceptions import GPTUnavaibleException
from bot.schemas.gpt import PromtSchema
from bot.schemas.tg_user import TGUserSchema
from bot.services.gpt import GPTService

router = Router(
    name=__name__
)

logger = logging.getLogger(__name__)


# Router responds to any text.
@router.message(F.text.startswith(''))
async def send_promt(
    message: Message,
) -> None:
    """Send promt."""

    # Dependencies

    gpt_service: GPTService = await get_gpt_service()

    # Schemas

    gpt_promt_schema = PromtSchema(text=message.text)

    tg_user_schema = TGUserSchema(
        id=message.from_user.id,
        username=message.from_user.username
    )

    # Process request

    try:
        gpt_response: str = await gpt_service.send_promt(
            tg_user_schema=tg_user_schema,
            promt_schema=gpt_promt_schema
        )
        await message.answer(text=gpt_response)
    except GPTUnavaibleException as e:
        await message.answer(text=e.detail)
    except Exception as e:
        logger.error(f'Unexpected_error: {e}')
        await message.answer('Неизвестная ошибка. Отправьте запрос повторно.')
