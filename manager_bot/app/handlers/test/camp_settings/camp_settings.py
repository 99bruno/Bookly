from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.keyboards.camp_settings.camp_settings import *

from app.templates.camp_settings.camp_settings import *

from sentry_logging.sentry_setup import sentry_sdk


router = Router()


@router.message(F.text == "Camp settings")
async def camp_settings_handler(message: types.Message):
    try:

        await message.answer(camp_settings_msg, reply_markup=camp_settings_kb)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)