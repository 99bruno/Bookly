
import os
from typing import Generator
import time

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sentry_logging.sentry_setup import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

bot = Bot(
    token=os.getenv("TOKEN_DANCER"), default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def send_notifications(message: str, users: Generator) -> None:
    try:
        for user in users:
            print(f"Try to send message to {user}")
            await bot.send_message(
                chat_id=user,
                text=message
            )
            time.sleep(1)
            print(f"Success, message sent to {user}")
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
        print("Error")
        print(e)
