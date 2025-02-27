import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from app.database.requests.check_user import get_admins
from app.database.requests.view_full_schedule.view_schedule import (
    fetch_lessons_with_full_info,
)
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logging.getLogger("aiogram").setLevel(logging.WARNING)

load_dotenv()

bot = Bot(
    token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def main() -> None:
    logger.info("Bot started successfully")
    try:
        while True:
            await fetch_lessons_with_full_info()
            for admin in await get_admins():
                try:
                    await bot.send_document(
                        chat_id=admin,
                        document=FSInputFile("app/database/schedule.xlsx"),
                        caption="Full schedule",
                        disable_notification=True,
                    )
                except Exception as e:
                    print(e)


            await asyncio.sleep(10800)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Successfully Exit")
