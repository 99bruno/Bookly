from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.keyboards.settings.settings import *
from app.scripts.settings.settings import restricted
from app.templates.settings.settings import *
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(Command("settings"))
@restricted
async def settings_handler(message: types.Message, state: FSMContext):
    try:
        await message.answer(settings_msg, reply_markup=settings_kb)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Back to settings")
@restricted
async def settings_handler(message: types.Message, state: FSMContext):
    try:
        await message.answer(settings_msg, reply_markup=settings_kb)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
