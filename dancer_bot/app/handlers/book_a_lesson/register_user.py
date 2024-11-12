import re

from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.database.requests.book_a_lesson.check_dancer import *
from app.database.requests.book_a_lesson.check_dancer import (
    add_couple,
    add_user,
    check_couple_registered,
    check_user_registered,
    check_user_registered_by_phone,
)
from app.keyboards.book_a_lesson.book_a_lesson import *
from app.keyboards.start.start import back_to_main_menu_keyboard
from app.scripts.auxiliary_functions.format_strings import format_string
from app.scripts.book_a_lesson.book_a_lesson import concatenate_couples, format_couple
from app.states.book_a_lesson.book_a_lesson import LessonRegistration
from app.states.book_a_lesson.register_dancer import (
    Couple,
    RegisterCouple,
    UserRegistration,
)
from app.templates.book_a_lesson.book_a_lesson import *
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(UserRegistration.phone_number)
async def command_book_a_lesson_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        if user_id := await check_user_registered_by_phone(
            message.contact.phone_number
        ):
            await update_dancer_info(
                user_id, message.from_user.username, message.from_user.id
            )
            await choose_partner(message, state)

        else:
            await state.update_data(phone_number=message.contact.phone_number)
            await state.set_state(UserRegistration.name)
            await message.answer(
                enter_name_message, reply_markup=types.ReplyKeyboardRemove()
            )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(UserRegistration.name)
async def command_book_a_lesson_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        if not re.compile(r"^[a-zA-Z'-]+$").match(coach_name := message.text):
            await message.answer(
                "<b>Упс, здається, щось не так із форматом введення імʼя 😕</b>\n\n"
                "Перевір себе 👀:\n"
                "• введено <b>лише імʼя</b>, без прізвища\n"
                "• імʼя написано <b>англійською</b> мовою\n\n"
                "<b>Давай спробуємо ще раз 🫂</b>"
            )
            return

        await state.update_data(name=coach_name)
        await state.set_state(UserRegistration.surname)
        await message.answer(enter_surname_message)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(UserRegistration.surname)
async def command_book_a_lesson_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        if not re.compile(r"^[a-zA-Z'-]+$").match(coach_surname := message.text):
            await message.answer(
                "<b>Хмм, здається щось не так із форматом введення прізвища 🤔</b>\n\n"
                "Перевір себе 👀:\n"
                "• прізвище введено <b>англійською мовою</b>\n"
                "• у прізвищі <b>нема пробілів</b>\n"
                "• введено <b>лише прізвище</b>, без імʼя\n\n"
                "<b>Спробуймо ще раз! 💙</b>"
            )
            return

        await state.update_data(surname=coach_surname)
        data = await state.get_data()

        await add_user(
            message.from_user.id,
            "TBA" if not message.from_user.username else message.from_user.username,
            data["phone_number"],
            data["name"],
            data["surname"],
            " ".join([data["name"], data["surname"]]),
            message.chat.id,
        )
        dancer_id = await check_user_registered_by_phone(data["phone_number"])
        await is_couple_registered(dancer_id, state, message)
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


async def is_couple_registered(
    dancer_id: int, state: FSMContext, message: types.Message
) -> None:
    try:
        couple_info = await check_couple_registered(dancer_id)

        if couple_info:
            await state.update_data(couples=couple_info)

            data = await state.get_data()

            couples = concatenate_couples(data["couples"])

            await message.answer(
                format_string(
                    choose_couple_message, ["\n".join(format_couple(couples))]
                ),
                reply_markup=create_keyboard_for_choose_couple(couples),
            )
        else:
            await register_couple(message)

        await state.clear()
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


async def register_couple(message: types.Message):
    try:
        await message.answer(
            register_couple_message, reply_markup=change_partner_solo_or_couple_keyboard
        )
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Соло")
async def command_book_a_lesson_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        dancer_id = await check_user_registered(message.from_user.id)

        if not await check_couple_exists(dancer_id, dancer_id):
            await add_couple(dancer_id, dancer_id)

        else:
            await message.answer("Ви вже зареєстровані як соло танцівник.")

        await choose_partner(message, state)
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "В парі")
async def command_book_a_lesson_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.set_state(RegisterCouple.phone_number)
        await message.answer(
            change_partner_phone_message, reply_markup=types.ReplyKeyboardRemove()
        )
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(RegisterCouple.phone_number)
async def handle_change_couple(message: types.Message, state: FSMContext) -> None:
    try:
        phone = (
            "".join(message.text.split())[1:]
            if message.text.startswith("+")
            else "".join(message.text.split())
        )

        if len(phone) != 12 or not phone.isdigit():
            await message.answer(
                "Упс, здається у тебе помилка у форматі введення номеру телефону 🫠\n\n"
                "Переконайся, що ти написав/-ла його у форматі  380XXXXXXXXX\n\n"
                "Спробуймо ще раз? 👇"
            )
            return

        await state.update_data(phone_number=phone)

        dancer2_id = await check_user_registered_by_phone(phone)

        if dancer2_id:
            if not await check_couple_exists(
                dancer1_id := await check_user_registered(message.from_user.id),
                dancer2_id,
            ):
                await add_couple(dancer1_id, dancer2_id)

                await state.update_data(
                    couples=await check_couple_registered(dancer1_id)
                )

                data = await state.get_data()

                couples = concatenate_couples(data["couples"])

                await message.answer(
                    format_string(
                        choose_couple_message, ["\n".join(format_couple(couples))]
                    ),
                    reply_markup=create_keyboard_for_choose_couple(couples),
                )

            else:
                await message.answer("<b>Ти вже зареєстрований з цим партнером)</b>")
                await choose_partner(message, state)

        else:
            await state.set_state(RegisterCouple.name)
            await message.answer(change_partner_name_message)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(RegisterCouple.name)
async def handle_change_couple(message: types.Message, state: FSMContext) -> None:
    try:
        if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
            await message.answer(
                "<b>Упс, здається, щось не так із форматом введення імʼя 😕</b>\n\n"
                "Перевір себе 👀:\n"
                "• введено <b>лише імʼя</b>, без прізвища\n"
                "• імʼя написано <b>англійською</b> мовою\n\n"
                "<b>Давай спробуємо ще раз 🫂</b>"
            )
            return

        await state.update_data(name=message.text)
        await state.set_state(RegisterCouple.surname)

        await message.answer(enter_surname_message)
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(RegisterCouple.surname)
async def handle_change_couple(message: types.Message, state: FSMContext) -> None:
    try:
        if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
            await message.answer(
                "<b>Хмм, здається щось не так із форматом введення прізвища 🤔</b>\n\n"
                "Перевір себе 👀:\n"
                "• прізвище введено <b>англійською мовою</b>\n"
                "• у прізвищі <b>нема пробілів</b>\n"
                "• введено <b>лише прізвище</b>, без імʼя\n\n"
                "<b>Спробуймо ще раз! 💙</b>"
            )
            return

        await state.update_data(surname=message.text)
        data = await state.get_data()

        await add_user(
            None,
            None,
            data["phone_number"],
            data["name"],
            data["surname"],
            " ".join([data["name"], data["surname"]]),
        )

        dancer_2 = await check_user_registered_by_phone(data["phone_number"])

        await add_couple(await check_user_registered(message.from_user.id), dancer_2)

        await choose_partner(message, state)
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


async def choose_partner(message: types.Message, state: FSMContext) -> None:
    try:
        await state.set_state(LessonRegistration.couples)
        await state.update_data(
            couples=await check_couple_registered(
                await check_user_registered(message.from_user.id)
            )
        )

        data = await state.get_data()

        couples = concatenate_couples(data["couples"])

        await message.answer(
            format_string(choose_couple_message, ["\n".join(format_couple(couples))]),
            reply_markup=create_keyboard_for_choose_couple(couples),
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
