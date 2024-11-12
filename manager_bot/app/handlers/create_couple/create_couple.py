import re

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from app.database.requests.create_couple.create_couple import *
from app.keyboards.create_couple.create_couple import *
from app.keyboards.start.start import *
from app.states.create_couple.create_couple import NewCouple
from app.templates.create_couple.create_couple import *
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(F.text == "Create couple")
async def camp_settings_handler(message: types.Message, state: FSMContext) -> None:
    try:
        await state.set_state(NewCouple.phone_1)
        await message.answer(
            create_couple_phone_message, reply_markup=types.ReplyKeyboardRemove()
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewCouple.phone_1, F.text)
async def phone_1_handler(message: types.Message, state: FSMContext) -> None:
    try:
        phone = (
            "".join(message.text.split())[1:]
            if message.text.startswith("+")
            else "".join(message.text.split())
        )

        if len(phone) != 12 or not phone.isdigit():
            await message.answer(
                "Oops, you seem to have an error in the phone number input format 🫠\n\n"
                "Make sure you write it in the format 380XXXXXXXXX\n\n"
                "Shall we try again? 👇"
            )
            return

        await state.update_data(phone_1=phone)

        if dancer_id := await check_user_registered_by_phone(phone):
            await state.update_data(dancer_id_1=dancer_id)
            await state.set_state(NewCouple.phone_2)
            await message.answer(create_couple2_phone_message)
        else:
            await message.answer(create_dancer_name_message)
            await state.set_state(NewCouple.name_1)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewCouple.phone_2, F.text)
async def phone_1_handler(message: types.Message, state: FSMContext) -> None:
    try:
        phone = (
            "".join(message.text.split())[1:]
            if message.text.startswith("+")
            else "".join(message.text.split())
        )

        if len(phone) != 12 or not phone.isdigit():
            await message.answer(
                "Oops, you seem to have an error in the phone number input format 🫠\n\n"
                "Make sure you write it in the format 380XXXXXXXXX\n\n"
                "Shall we try again? 👇"
            )
            return

        await state.update_data(phone_2=phone)

        data = await state.get_data()

        if dancer_id := await check_user_registered_by_phone(phone):
            await state.update_data(dancer_id_2=dancer_id)
            if await check_couple_exists(data["dancer_id_1"], dancer_id):
                await message.answer(
                    "This pair already exists in the system 🤔\n\n"
                    "Please try again with another phone number"
                )
                return
            else:
                await add_couple(data["dancer_id_1"], dancer_id)
                await message.answer("The pair has been successfully created 🎉")
                await message.answer(
                    "What would you like to do next?", reply_markup=start_keyboard
                )
        else:
            await message.answer(create_dancer_name_message)
            await state.set_state(NewCouple.name_2)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewCouple.name_1, F.text)
async def name_1_handler(message: types.Message, state: FSMContext) -> None:
    try:
        if not re.compile(r"^[a-zA-Z'-]+$").match(coach_name := message.text):
            await message.answer(
                "<b>Oops, something seems wrong with the name input format 😕</b>\n\n"
                "Check yourself 👀:\n"
                "• entered <b>first name only</b>, no last name\n"
                "• the name is written in <b>English</b> language\n\n"
                "<b>Let's try again 🫂</b>"
            )
            return

        await state.update_data(name_1=message.text)

        await state.set_state(NewCouple.surname_1)
        await message.answer(create_dancer_surname_message)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewCouple.surname_1, F.text)
async def surname_1_handler(message: types.Message, state: FSMContext) -> None:
    try:
        if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
            await message.answer(
                "<b>Hmm, something seems wrong with the last name input format 🤔</b>\n\n"
                "Check yourself 👀:\n"
                "• the last name is entered in <b>English</b>\n"
                "• there are <b>no spaces in the last name</b>\n"
                "• entered <b>last name only</b>, no first name\n\n"
                "<b>Let's try again! 💙</b>"
            )
            return

        await state.update_data(surname_2=message.text)

        data = await state.get_data()

        await add_user(
            tg_id=message.from_user.id,
            tg_username=message.from_user.username,
            phone_number=data["phone_1"],
            name=data["name_1"],
            surname=message.text,
            full_name=data["name_1"] + " " + message.text,
        )

        await state.set_state(NewCouple.phone_2)
        await message.answer(create_couple2_phone_message)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewCouple.name_2, F.text)
async def name_1_handler(message: types.Message, state: FSMContext) -> None:
    try:
        if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
            await message.answer(
                "<b>Oops, something seems wrong with the name input format 😕</b>\n\n"
                "Check yourself 👀:\n"
                "• entered <b>first name only</b>, no last name\n"
                "• the name is written in <b>English</b> language\n\n"
                "<b>Let's try again 🫂</b>"
            )
            return

        await state.update_data(name_2=message.text)

        await state.set_state(NewCouple.surname_2)
        await message.answer(create_dancer_surname_message)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewCouple.surname_2, F.text)
async def surname_1_handler(message: types.Message, state: FSMContext) -> None:
    try:
        if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
            await message.answer(
                "<b>Hmm, something seems wrong with the last name input format 🤔</b>\n\n"
                "Check yourself 👀:\n"
                "• the last name is entered in <b>English</b>\n"
                "• there are <b>no spaces in the last name</b>\n"
                "• entered <b>last name only</b>, no first name\n\n"
                "<b>Let's try again! 💙</b>"
            )
            return

        await state.update_data(surname_2=message.text)

        data = await state.get_data()

        await add_user(
            tg_id=message.from_user.id,
            tg_username=message.from_user.username,
            phone_number=data["phone_2"],
            name=data["name_2"],
            surname=message.text,
            full_name=data["name_2"] + " " + message.text,
        )

        await add_couple(
            await check_user_registered_by_phone(data["phone_1"]),
            await check_user_registered_by_phone(data["phone_2"]),
        )
        await message.answer("The pair has been <b>successfully created</b> 🎉")
        await message.answer(
            "What would you like to do next?", reply_markup=start_keyboard
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
