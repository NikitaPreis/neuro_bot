"""
Handlers for bot commands.
"""
from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message

from bot import text

router = Router(
    name=__name__
)


@router.message(Command('start'))
async def cmd_start(message: Message) -> None:
    """Start command."""
    await message.answer(text.greet)


@router.message(F.text.lower() == 'help')
@router.message(F.text.lower() == 'помощь')
@router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    """Help command."""
    await message.answer(text.help)
