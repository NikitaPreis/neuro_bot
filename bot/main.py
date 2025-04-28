import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.database.accessor import init_models
from bot.handlers import commands_router, gpt_router
from bot.settings import Settings


async def run_bot(settings: Settings):
    """Run bot."""
    bot = Bot(token=settings.telegram.BOT_API_TOKEN)

    dp = Dispatcher()

    dp.include_router(commands_router)
    dp.include_router(gpt_router)

    await dp.start_polling(bot, skip_updates=True)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        filename='neuro_bot.log',
        filemode='a',
        format='%(asctime)s, %(lineno)d, %(levelname)s, %(message)s, %(name)s',
        encoding='utf-8'
    )

    await init_models()

    settings = Settings.load()

    await run_bot(settings=settings)


if __name__ == '__main__':
    asyncio.run(main())
