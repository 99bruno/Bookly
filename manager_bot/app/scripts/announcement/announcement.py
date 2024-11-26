
import os
from typing import Generator

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

bot = Bot(
    token=os.getenv("TOKEN_DANCER"), default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def send_notifications(message: str, users: Generator) -> None:
    try:
        for user in users:
            await bot.send_message(
                chat_id=user,
                text=message
            )
    except :
        pass
