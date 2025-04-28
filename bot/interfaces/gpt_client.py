from abc import ABC, abstractmethod
from typing import Any

from bot.schemas.gpt import PromtSchema


class AbstractGPTClient(ABC):
    """Abstract class for GPT Clients."""

    @abstractmethod
    async def send_promt(self, promt_schema: PromtSchema) -> Any:
        """Send promt to GPT and get reponse."""
        pass
