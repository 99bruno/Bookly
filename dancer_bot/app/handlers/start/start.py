from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.keyboards.start.start import start_keyboard
from app.templates.start.start import start_message_1, start_message_2
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    try:
        await state.clear()
        await message.answer(start_message_1)
        await message.answer(
            start_message_2, reply_markup=start_keyboard, parse_mode="HTML"
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Повернутись в головне меню")
async def command_back_to_main_menu_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.clear()
        await message.answer(start_message_2, reply_markup=start_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda query: query.data == "back_to_main_menu")
async def command_back_to_main_menu_callback_handler(
    query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        await state.clear()
        await query.message.answer(start_message_2, reply_markup=start_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
