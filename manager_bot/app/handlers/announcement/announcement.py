from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from app.states.announcement.announcement import *
from app.scripts.announcement.announcement import *
from app.database.requests.announcement.announcement import *
from app.keyboards.announcement.announcement import *
from app.templates.announcement.announcement import *
from sentry_logging.sentry_setup import sentry_sdk


router = Router()


@router.message(F.text == "Make a announcement 📢")
async def camp_settings_handler(message: types.Message) -> None:
    try:
        await message.answer(announcements_main_message, reply_markup=announcements_main_kb)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Send a message to all users 📢")
async def camp_settings_handler(message: types.Message, state: FSMContext) -> None:
    try:
        await message.answer(announcements_all_users_message, reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(users_id=set(await get_all_user_id()))

        await state.set_state(Announcement.msg)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(Announcement.msg)
async def camp_settings_handler(message: types.Message, state: FSMContext) -> None:
    try:
        print("Message state")
        print((await state.get_data()).get("users_id"))
        await send_notifications(message.text, (await state.get_data()).get("users_id"), message)
        print("Message sent")

        await message.answer(announcements_all_users_confirmation_message, reply_markup=announcements_main_kb)
        await state.clear()

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Send a message by coach booking 📢")
async def camp_settings_handler(message: types.Message, state: FSMContext) -> None:
    try:
        coaches = await get_all_coaches()
        await message.answer(announcements_choose_coach_message, reply_markup=announcements_choose_coach_kb(coaches))

        await state.update_data(coaches=coaches)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(F.data.startswith("message_by_coach"))
async def camp_settings_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    try:
        coach_id = int(query.data.split("_")[-1])
        coach = (await state.get_data()).get("coaches")[coach_id]

        await query.message.answer(announcements_all_users_message, reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(users_id=set(await get_user_id_by_coach_id(int(coach["id"]))))

        await state.set_state(Announcement.msg)

    except Exception as e:
        print(e)
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)
