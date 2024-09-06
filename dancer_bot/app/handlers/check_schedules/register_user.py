import re

from aiogram import types, html, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


from app.templates.book_a_lesson.book_a_lesson import *

from app.keyboards.start.start import back_to_main_menu_keyboard
from app.keyboards.book_a_lesson.book_a_lesson import *

from app.database.requests.book_a_lesson.check_dancer import *

from app.scripts.auxiliary_functions.format_strings import format_string
from app.scripts.book_a_lesson.book_a_lesson import concatenate_couples, format_couple

from app.states.book_a_lesson.register_dancer import UserRegistration, RegisterCouple

from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(UserRegistration.phone_number)
async def command_book_a_lesson_handler(message: types.Message, state: FSMContext) -> None:
    try:

        if user_id := await check_user_registered_by_phone(message.contact.phone_number):
            await update_dancer_info(user_id, message.from_user.username, message.from_user.id)
            await is_couple_registered(message, state)

        await state.update_data(phone_number=message.contact.phone_number)
        await state.set_state(UserRegistration.name)
        await message.answer(enter_name_message, reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(UserRegistration.name)
async def command_book_a_lesson_handler(message: types.Message, state: FSMContext) -> None:
    try:

        if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
            await message.answer("Будь ласка, введіть ім'я англійською мовою.")
            return

        await state.update_data(name=message.text)
        await state.set_state(UserRegistration.surname)
        await message.answer(enter_surname_message)
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(UserRegistration.surname)
async def command_book_a_lesson_handler(message: types.Message, state: FSMContext) -> None:
    try:

        if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
            await message.answer("Будь ласка, введіть ім'я англійською мовою.")
            return

        await state.update_data(surname=message.text)
        data = await state.get_data()

        try:
            await add_user(message.from_user.id, message.from_user.username, data["phone_number"], data["name"],
                           data["surname"], " ".join([data["name"], data["surname"]]))
            dancer_id = await check_user_registered_by_phone(data["phone_number"])
            await is_couple_registered(dancer_id, state, message)
        except:
            pass
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


async def is_couple_registered(dancer_id: int, state: FSMContext, message: types.Message) -> None:
    try:
        couple_info = await check_couple_registered(dancer_id)

        if couple_info:
            pass
        else:
            await message.answer(couple_not_found_in_db_message, reply_markup=confirm_book_lessons_keyboard)

        await state.clear()
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)

