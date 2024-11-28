import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from app.database.requests.analysis.analysis import get_lessons_counts
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logging.getLogger("aiogram").setLevel(logging.WARNING)

load_dotenv()

bot = Bot(
    token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


def dj_template(lessons: tuple) -> str:
    return (f"Hi, Jonathan! It is daily update on amount of booked lessons from <b>Pasha</b> and <b>Nastya</b>)\n\n"
            f"Today {lessons[0]}/{lessons[1]-(lessons[2]-lessons[0])} ~ "
            f"{lessons[0]/(lessons[1]-(lessons[2]-lessons[0])) * 100:.1f} % lessons are booked\n\n"
            f"Have a great day 💛")


async def main() -> None:
    logger.info("Bot started successfully")
    try:
        while True:
            info = await get_lessons_counts()
            for user in [482576057, 377081695]:
                await bot.send_message(
                    chat_id=user,
                    text=dj_template(info),
                )
            await asyncio.sleep(86400)
    except:
        print("Error")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Successfully Exit")