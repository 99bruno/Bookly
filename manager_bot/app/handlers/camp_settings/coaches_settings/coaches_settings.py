from aiogram import types, Router, F

from app.keyboards.camp_settings.coaches_settings.coaches_settings import *

from app.templates.camp_settings.coaches_settings.coaches_settings import *

from sentry_logging.sentry_setup import sentry_sdk


router = Router()


@router.message(F.text == "Coaches settings 🕺💃")
async def coaches_settings_handler(message: types.Message):
    try:

        await message.answer(coaches_settings_msg, reply_markup=coaches_settings_kb)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
