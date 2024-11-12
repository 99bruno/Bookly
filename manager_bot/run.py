import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.database.models import async_main
from app.handlers import register_all_handlers
from app.middleware.check_access import AccessControlMiddleware
from app.middleware.delete_messges import AccessMiddleware
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger("aiogram").setLevel(logging.WARNING)

load_dotenv()

bot = Bot(
    token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

latest_messages = {}

dp.message.middleware(AccessMiddleware(bot, latest_messages))
dp.message.middleware(AccessControlMiddleware())


async def main() -> None:
    await async_main()

    dp.include_router(register_all_handlers())

    logger.info("Bot started successfully")

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Successfully Exit")
