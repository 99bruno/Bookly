import datetime

from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from app.database.requests.book_a_lesson.book_a_lesson import *
from app.database.requests.book_a_lesson.check_dancer import (
    add_couple,
    add_user,
    check_couple_registered,
    check_user_registered,
    check_user_registered_by_phone,
)
from app.database.requests.check_schedules.check_schedules import *
from app.keyboards.book_a_lesson.book_a_lesson import (
    confirm_book_lessons_keyboard,
    share_contact_keyboard,
)
from app.keyboards.check_schedules.check_schedules import *
from app.keyboards.start.start import start_keyboard
from app.scripts.auxiliary_functions.format_strings import format_string
from app.scripts.book_a_lesson.book_a_lesson import (
    concatenate_couples,
    format_couple,
    format_lesson_info,
)
from app.scripts.check_schedules.check_schedules import *
from app.states.check_schedules.register_dancer import Couple, UserRegistration
from app.templates.book_a_lesson.book_a_lesson import enter_phone_number_message
from app.templates.check_schedules.check_schedules import *
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(F.text == "Мої бронювання 🕒")
async def command_book_a_lesson_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.clear()

        user_info = await check_user_registered(message.from_user.id)
        if user_info:
            couple_info = await check_couple_registered(user_info)
            if couple_info:
                await state.set_state(Couple.couples)
                await state.update_data(couples=couple_info)

                couples = concatenate_couples(couple_info)

                await message.answer(
                    format_string(
                        choose_couple_message, ["\n".join(format_couple(couples))]
                    ),
                    reply_markup=create_keyboard_for_choose_couple_for_schedule(
                        couples
                    ),
                )

            else:
                await message.answer(
                    couple_not_found_in_db_message,
                    reply_markup=confirm_book_lessons_keyboard,
                )
        else:
            await state.set_state(UserRegistration.phone_number)
            await message.answer(
                enter_phone_number_message, reply_markup=share_contact_keyboard
            )
            await message.answer_photo(
                photo=FSInputFile("app/database/Share_contact.jpeg")
            )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data.startswith("schedules_couple_"))
async def handle_couple_selection(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        couple_id = callback_query.data.split("_")[-1]

        await state.set_state(Couple.current_couple)
        await state.update_data(couple_id=couple_id)
        data = await state.get_data()

        lessons = await get_booked_lessons_by_couple(
            data["couples"][int(couple_id)]["couple_id"]
        )

        await state.update_data(lessons=lessons)

        await callback_query.message.answer(
            format_string(
                check_schedules_message,
                [
                    data["couples"][int(couple_id)]["dancer1_full_name"]
                    + " та "
                    + data["couples"][int(couple_id)]["dancer2_full_name"],
                    await format_booked_lessons(lessons),
                ],
            ),
            reply_markup=check_schedules_keyboard,
        )
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data == "back_to_couples")
async def cancel_booking_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    try:
        couple_info = await check_couple_registered(
            await check_user_registered(query.from_user.id)
        )

        await state.set_state(Couple.couples)
        await state.update_data(couples=couple_info)

        couples = concatenate_couples(couple_info)

        await query.message.edit_text(
            format_string(choose_couple_message, ["\n".join(format_couple(couples))])
        )
        await query.message.edit_reply_markup(
            reply_markup=create_keyboard_for_choose_couple_for_schedule(couples)
        )
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data == "cancel_lesson")
async def cancel_booking_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    try:
        data = await state.get_data()

        await query.message.edit_reply_markup(
            reply_markup=create_keyboard_for_cancel_lesson(
                sorted_lessons := await sort_lessons(data["lessons"])
            )
        )

        await state.update_data(sorted_lessons=sorted_lessons)
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data.startswith("cancel_lesson_"))
async def handle_cancel_booking(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        lesson_id = callback_query.data.split("_")[-1]
        data = await state.get_data()

        await state.update_data(
            lesson_id=data["sorted_lessons"][lesson_id], lesson_date=lesson_id
        )
        await state.set_state(Couple.reason)

        await callback_query.message.answer(
            cancel_lesson_reason_message, reply_markup=types.ReplyKeyboardRemove()
        )
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data == "return_to_schedule")
async def cancel_booking_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    try:
        data = await state.get_data()

        await query.message.edit_text(
            format_string(
                check_schedules_message,
                [
                    data["couples"][int(data["couple_id"])]["dancer1_full_name"]
                    + " та "
                    + data["couples"][int(data["couple_id"])]["dancer2_full_name"],
                    await format_booked_lessons(data["lessons"]),
                ],
            ),
            reply_markup=check_schedules_keyboard,
        )
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(Couple.reason)
async def handle_cancel_reason(message: types.Message, state: FSMContext) -> None:
    try:
        await state.update_data(reason=message.text)
        await state.set_state(Couple.confirm)
        data = await state.get_data()

        await message.answer(
            format_string(cancel_lesson_confirmation_message, [data["lesson_date"]]),
            reply_markup=confirm_lesson_cancel_keyboard,
        )
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Скасувати урок")
async def cancel_booking_handler(message: types.Message, state: FSMContext) -> None:
    try:
        data = await state.get_data()

        await cancel_booked_lesson(data["lesson_id"], data, message.from_user.username)

        await message.answer(cancel_lesson_message, reply_markup=start_keyboard)
        await state.clear()
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data == "reschedule_lesson")
async def move_booking_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    try:
        data = await state.get_data()

        await query.message.edit_reply_markup(
            reply_markup=create_keyboard_for_reschedule_lesson(
                sorted_lessons := await sort_lessons_test(data["lessons"])
            )
        )

        await state.update_data(sorted_lessons=sorted_lessons)
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data == "return_to_reschedule")
async def cancel_booking_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    try:
        data = await state.get_data()

        await query.message.edit_text(
            format_string(
                check_schedules_message,
                [
                    data["couples"][int(data["couple_id"])]["dancer1_full_name"]
                    + " та "
                    + data["couples"][int(data["couple_id"])]["dancer2_full_name"],
                    await format_booked_lessons(data["lessons"]),
                ],
            )
        )

        await query.message.edit_reply_markup(
            reply_markup=create_keyboard_for_reschedule_lesson(
                sorted_lessons := await sort_lessons_test(data["lessons"])
            )
        )

        await state.update_data(sorted_lessons=sorted_lessons)
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data.startswith("reschedule_lesson_"))
async def handle_reschedule_booking(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        lesson_id = callback_query.data.split("_")[-1]
        data = await state.get_data()

        await callback_query.message.edit_text(
            format_string(
                reschedule_lesson_message,
                [await get_coach_name(data["sorted_lessons"][lesson_id])],
            )
        )
        await callback_query.message.edit_reply_markup(
            reply_markup=create_keyboard_for_confirm_reschedule_lesson(
                available_lessons := await get_available_lessons_by_lesson_id(
                    data["sorted_lessons"][lesson_id]
                )
            )
        )

        await state.update_data(
            available_lessons=available_lessons,
            lesson_id=data["sorted_lessons"][lesson_id],
        )
    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data.startswith("lesson_reschedule"))
async def handle_reschedule_lesson(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        lesson_id = callback_query.data.split("lesson_reschedule")[-1]

        data = await state.get_data()

        response = await reschedule_lesson(
            data["lesson_id"], data["available_lessons"][int(lesson_id)]["id"]
        )

        if response:
            await callback_query.message.answer(
                reschedule_lesson_confirmation_message, reply_markup=start_keyboard
            )
            await state.clear()
        else:
            await callback_query.answer(
                "Виберіть інший урок, цей нажаль зайнятий(", show_alert=True
            )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)
