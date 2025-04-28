import json
import logging
import uuid
from dataclasses import dataclass

import httpx
from pydantic import ValidationError

from bot.exceptions import (GPTClientAccessTokenException, GPTClientException,
                            GPTClientHTTPException)
from bot.interfaces import AbstractGPTClient
from bot.schemas.gpt import (GigaChatAccessTokenSchema, GPTResponseSchema,
                             PromtSchema)
from bot.settings import Settings

logger = logging.getLogger(__name__)


@dataclass
class GigaChatClient(AbstractGPTClient):
    async_client: httpx.AsyncClient
    settings: Settings

    async def send_promt(
        self,
        promt_schema: PromtSchema
    ) -> GPTResponseSchema:
        """Send promt to Giga Chat and get response."""

        try:
            access_token_schema = await self._get_access_token()
        except (GPTClientAccessTokenException, GPTClientException) as e:
            logging.error(e.detail)
            raise GPTClientException

        try:
            gpt_response_schema: GPTResponseSchema = (
                await self._send_promt(
                    msg=promt_schema.text,
                    access_token=access_token_schema.access_token
                )
            )
        except GPTClientHTTPException as e:
            logging.error(e.detail)
            raise GPTClientException
        return gpt_response_schema

    async def _get_access_token(self) -> GigaChatAccessTokenSchema:
        """
        Get GigaChat access token.

        Giga Chat API sets a limit: no more than 10 tokens per second.
        """

        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
            'Authorization': f'Basic {
                               self.settings.giga_chat.GIGA_CHAT_AUTH_KEY
                              }'
        }

        # To avoid 'verify=False' we should install certificate:
        # https://developers.sber.ru/docs/ru/gigachat/certificates

        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url=self.settings.giga_chat.GIGA_CHAT_AUTH_URL,  # auth url
                headers=headers,
                data=payload,
            )

        await self._check_status_code_is_ok(
            status_code=response.status_code, response_text=response.text
        )

        try:
            auth_token_data = response.json()
            return GigaChatAccessTokenSchema(
                access_token=auth_token_data.get('access_token'),
                expires_at=auth_token_data.get('expires_at')
            )
        except ValidationError as e:
            logging.error(e)
            raise GPTClientAccessTokenException

    async def _send_promt(
        self,
        msg: str,
        access_token: str
    ) -> GPTResponseSchema:
        """Send promt to Giga Chat."""

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'applications/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = json.dumps({
            'model': 'GigaChat',
            'messages': [
                {
                    'role': 'user',
                    'content': msg
                },
            ]
        })

        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url=self.settings.giga_chat.GIGA_CHAT_REQUEST_URL,
                headers=headers,
                data=payload
            )

        await self._check_status_code_is_ok(
            status_code=response.status_code,
            response_text=response.text
        )

        gpt_response = response.json()['choices'][0]['message']['content']
        return GPTResponseSchema(
            response_text=gpt_response
        )

    async def _check_status_code_is_ok(
        self,
        status_code: int,
        response_text: str
    ) -> None:
        """Check that status code is ok."""
        if status_code != httpx.codes.OK:
            logging.error(
                'Giga Chat клиент получил неожиданный ответ '
                f'status code: {status_code} '
                f'response text: {response_text}'
            )
            raise GPTClientHTTPException
