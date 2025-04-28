import logging
from dataclasses import dataclass

from bot.exceptions import (DataBaseException, GPTClientException,
                            GPTUnavaibleException)
from bot.interfaces import AbstractGPTClient, AbstractRepository
from bot.schemas.gpt import (GPTMessageSessionSchema, GPTResponseSchema,
                             PromtSchema)
from bot.schemas.tg_user import TGUserSchema

logger = logging.getLogger(__name__)


@dataclass
class GPTService:
    """GPT Serivice."""

    gpt_client: AbstractGPTClient
    message_repo: AbstractRepository
    user_repo: AbstractRepository

    async def send_promt(
        self,
        tg_user_schema: TGUserSchema,
        promt_schema: PromtSchema
    ) -> str:
        """Send promt to GPT and return result."""

        try:
            gpt_response_schema: GPTResponseSchema = (
                await self.gpt_client.send_promt(promt_schema=promt_schema)
            )
        except GPTClientException as e:
            logging.error(e.detail)
            raise GPTUnavaibleException

        gpt_message_session_schema = GPTMessageSessionSchema(
            request_text=promt_schema.text,
            response_text=gpt_response_schema.response_text,
            user_id=tg_user_schema.id
        )

        # Save telegram user, request message and gpt response.
        try:
            await self._create_user_if_not_exists(
                user_schema=tg_user_schema
            )
            await self.message_repo.create(
                model_schema=gpt_message_session_schema
            )
        except DataBaseException as e:
            # We can send a GPT response to the user,
            # but the messages context will be lost.
            logging.error(e.detail)

        return gpt_response_schema.response_text

    async def _create_user_if_not_exists(
        self,
        user_schema: TGUserSchema
    ) -> int:
        """Create user if user not exists."""

        user_id = await self.user_repo.exists(model_schema=user_schema)
        if not await self.user_repo.exists(model_schema=user_schema):
            user_id = await self.user_repo.create(
                model_schema=user_schema
            )
        return user_id
