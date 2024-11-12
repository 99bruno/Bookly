from aiogram import F, Router, types
from aiogram.client.bot import Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.keyboards.start.start import start_keyboard
from app.scripts.auxiliary_functions.delete_messages import (
    delete_previous_messages_bot,
    delete_previous_messages_user,
)
from app.templates.start.start import back_main_menu_message, start_message
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    try:
        await state.clear()

        await message.answer(start_message, reply_markup=start_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Back to the main menu")
async def command_back_to_main_menu_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.clear()

        await message.answer(back_main_menu_message, reply_markup=start_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(
    lambda callback_query: callback_query.data == "back_to_main_menu"
)
async def command_back_to_main_menu_handler(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        await state.clear()

        await callback.message.answer(
            back_main_menu_message, reply_markup=start_keyboard
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback.from_user.id)
            scope.set_extra("username", callback.from_user.username)

        sentry_sdk.capture_exception(e)
