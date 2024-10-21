from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.keyboards.camp_settings.schedule_settings.unblock_lesson import *

from app.templates.camp_settings.schedule_settings.unblock_lesson import *

from app.database.requests.schedule_settings.unblock_lesson import *

from app.states.schedule_settings.unblock_lesson import *

from sentry_logging.sentry_setup import sentry_sdk


router = Router()


@router.message(F.text == "Unblock lesson ✅")
async def command_block_lesson_handler(message: types.Message) -> None:
    try:

        await message.answer(dates_message,
                             reply_markup=await dates_keyboard(await get_days_of_camp()))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(F.data == "return_to_dates_of_unblocking")
async def command_return_to_dates_of_blocking_handler(callback_query: types.CallbackQuery) -> None:
    try:

        await callback_query.message.edit_text(dates_message)
        await callback_query.message.edit_reply_markup(reply_markup=await dates_keyboard(await get_days_of_camp()))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(F.data.startswith("date_choose_unblock_"))
async def command_block_date_choose_handler(callback_query: types.CallbackQuery,
                                            state: FSMContext) -> None:
    try:
        coaches = await get_coach_by_a_date(current_date := callback_query.data.split("_")[-1])

        await state.update_data(current_date=current_date)
        await callback_query.message.edit_text(coach_message)
        await callback_query.message.edit_reply_markup(reply_markup=await create_keyboard_for_coaches(coaches))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(F.data.startswith("choose_coach__unblock_"))
async def command_block_coach_choose_handler(callback_query: types.CallbackQuery,
                                             state: FSMContext) -> None:
    try:
        data = await state.get_data()

        lessons = await get_lessons_by_a_coach_and_date_and_not_booked(current_coach := callback_query.data.split("_")[-1],
                                                                   data["current_date"])

        await state.update_data(current_coach=current_coach, avaible_lessons=lessons)

        await callback_query.message.edit_text(time_message)
        await callback_query.message.edit_reply_markup(reply_markup=await create_keyboard_for_lessons(lessons))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(F.data.startswith("choose_lesson_unblock__"))
async def command_block_lesson_choose_handler(callback_query: types.CallbackQuery,
                                              state: FSMContext) -> None:
    try:
        lesson_block = callback_query.data.split("__")[-1].split("_")

        await unblock_lesson_by_id(lesson_block[-1])

        data = await state.get_data()

        del data["avaible_lessons"][lesson_block[0]]

        await state.update_data(avaible_lessons=data["avaible_lessons"])

        await callback_query.answer("Lesson unblocked", show_alert=True)

        await callback_query.message.edit_reply_markup(reply_markup=await create_keyboard_for_lessons(data["avaible_lessons"]))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(F.data == "return_to_coaches_of_unblocking")
async def command_return_to_coaches_of_blocking_handler(callback_query: types.CallbackQuery,
                                                        state: FSMContext) -> None:
    try:
        data = await state.get_data()

        coaches = await get_coach_by_a_date(data["current_date"])

        await callback_query.message.edit_text(coach_message)
        await callback_query.message.edit_reply_markup(reply_markup=await create_keyboard_for_coaches(coaches))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
