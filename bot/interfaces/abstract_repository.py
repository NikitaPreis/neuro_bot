from abc import ABC, abstractmethod
from typing import NoReturn


class AbstractRepository(ABC):
    """Interface for repositories."""

    @abstractmethod
    async def get(self) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def create(self) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def exists(self) -> NoReturn:
        raise NotImplementedError
