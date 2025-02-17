from datetime import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaDocument
from app.database.requests.view_full_schedule.view_schedule import *
from app.database.requests.schedules.Schedule_for_coach import *
from app.templates.view_full_schedule.view_full_schedule import *
from app.database.requests.schedules.Schedule_for_couple import *
from app.keyboards.schedules.schedules import *
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(F.text == "Schedules")
async def command_schedules_handler(message: types.Message) -> None:
    try:
        await message.answer(
            "Choose what you want to do",
            reply_markup=schedules_keyboard,
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "View full schedule in Excel")
async def command_view_full_schedule_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.clear()

        await fetch_lessons_with_full_info()

        await message.answer_document(
            FSInputFile("app/database/schedule.xlsx"), caption=view_schedule_message
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "View full schedule for each couple")
async def command_view_full_schedule_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.clear()

        await get_lesson_for_each_couple()

        await message.answer_document(
            FSInputFile("app/database/couple_schedule.pdf"), caption="Here is the couple Schedule"
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "View full schedule for each coach")
async def command_view_full_schedule_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.clear()

        await get_lesson_for_each_coach()

        await message.answer_document(
            FSInputFile("app/database/coach_schedule.pdf"), caption="Here is the coach Schedule 📅",
            reply_markup=await create_schedule_keyboard(await get_dates_of_event())
        )

    except Exception as e:
        print(e)
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data.startswith("schedule_coach_for_"))
async def schedule_coach_for_date_handler(query: types.CallbackQuery) -> None:
    try:
        date = query.data.split("_")[-1].split()[0]

        await get_lesson_for_each_coach_for_date(date)
        await query.message.answer_document(
            FSInputFile(f"app/database/coach_schedule_{date}.pdf"), caption=f"Here is the coach Schedule for {date}📅",
            reply_markup=await create_schedule_keyboard(await get_dates_of_event())
        )

    except Exception as e:
        print(e)
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)