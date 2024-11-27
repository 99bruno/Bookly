from aiogram import F, Router, types

from app.scripts.analysis.analysis import *
from app.database.requests.analysis.analysis import *
from app.keyboards.analysis.analysis import *
from sentry_logging.sentry_setup import sentry_sdk


router = Router()


@router.message(F.text == "Analysis 🔬")
async def camp_settings_handler(message: types.Message) -> None:
    try:
        await message.answer(await analysis_booked_lessons_unpack(await get_lessons_counts()), reply_markup=add_coach_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
        print(e)


@router.callback_query(lambda c: c.data == "analysis_booked_lessons")
async def camp_settings_handler(query: types.CallbackQuery) -> None:
    try:
        await query.message.edit_text(await analysis_booked_lessons_unpack(await get_lessons_counts()), reply_markup=add_coach_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)
        print(e)


@router.callback_query(lambda c: c.data == "analysis_coaches_booking_rating")
async def analysis_coaches_booking_rating_handler(query: types.CallbackQuery) -> None:
    try:
        await query.message.edit_text(await analysis_coaches_booking_rating_unpack(await get_coach_lessons_summary()), reply_markup=add_coach_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda c: c.data == "analysis_coaches_with_available_lessons")
async def analysis_coaches_with_available_lessons_handler(query: types.CallbackQuery) -> None:
    try:
        await query.message.edit_text(await analysis_coaches_with_available_lessons_unpack(await get_available_lessons_summary()), reply_markup=add_coach_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)
        print(e)


@router.callback_query(lambda c: c.data == "analysis_overall_income")
async def analysis_overall_income_handler(query: types.CallbackQuery) -> None:
    try:
        await query.message.edit_text(await analysis_overall_income_unpack(await get_lessons_financial_summary()), reply_markup=add_coach_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)
        print(e)