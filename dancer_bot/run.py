import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.handlers import register_all_handlers
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


async def main() -> None:
    dp.include_router(register_all_handlers())

    logger.info(" Bot started successfully")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Successfully Exit")
