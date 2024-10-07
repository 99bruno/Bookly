from datetime import datetime
import re

from aiogram import types, Router, F
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext

from app.keyboards.settings.create_event import *
from app.keyboards.start.start import start_keyboard

from app.templates.settings.create_event import *

from app.states.create_event.create_event import NewEvent

from app.scripts.create_event.create_event import *
from app.scripts.settings.settings import restricted
from app.scripts.auxiliary_functions.delete_messages import delete_previous_messages_bot, delete_previous_messages_user

from app.database.requests.create_event.create_event import add_event_with_schedule

from sentry_logging.sentry_setup import sentry_sdk


router = Router()


@router.message(F.text == "Create a new event")
@restricted
async def command_coaches_handler(message: types.Message,
                                  state: FSMContext) -> None:

    try:

        await state.clear()

        await message.answer(create_event_message, reply_markup=confirm_create_event_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)



@router.message(F.text == "Decline")
@restricted
async def decline_handler(message: types.Message,
                          state: FSMContext) -> None:

    try:

        await message.answer(decline_message, reply_markup=start_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Create new event")
@restricted
async def confirm_handler(message: types.Message,
                          state: FSMContext) -> None:
    try:

        await state.set_state(NewEvent.name)

        await message.answer(add_name_message, reply_markup=types.ReplyKeyboardRemove())

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewEvent.name)
@restricted
async def add_name_handler(message: types.Message,
                           state: FSMContext) -> None:

    try:

        name = message.text

        if len(name) > 50:
            answer = await message.answer("The name is too long. Please try again.")
            latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
            return

        await state.update_data(name=message.text)

        await state.set_state(NewEvent.dates)

        await message.answer(add_date_message.format(name))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)



@router.message(NewEvent.dates)
@restricted
async def add_date_handler(message: types.Message,
                           state: FSMContext) -> None:
    try:
        dates = message.text

        data_correctness, date_answer = validate_date_range(dates)

        if not data_correctness:
            answer = await message.answer(f"{date_answer}\n\nPlease try again using the format: DD.MM.YYYY-DD.MM.YYYY")
            latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
            return

        await state.update_data(dates=date_answer)
        await state.update_data(start_time=None, end_time=None, lesson_duration=None, breaks=None)

        await state.set_state(NewEvent.type_of_schedule)

        await message.answer(add_schedule_message, reply_markup=type_of_schedule_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)



@router.callback_query(NewEvent.type_of_schedule)
@restricted
async def add_schedule_handler(callback_query: types.CallbackQuery,
                               state: FSMContext) -> None:
    try:

        if callback_query.data == "single_template":
            dates = await state.get_data()
            await state.set_state(NewEvent.single_template)



            await callback_query.message.answer(
                single_template_message_unpack(
                    template=single_template_message,
                    data=dates
                ),
                reply_markup=single_template_keyboard)

        elif callback_query.data == "multiple_templates":
            await state.set_state(NewEvent.multiple_templates)
            await callback_query.answer("Ops.. We are currently working on this function, you’ll be able to use it soon!",
                                        show_alert=True)


    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(NewEvent.single_template)
@restricted
async def single_template_handler(callback_query: types.CallbackQuery,
                                  state: FSMContext) -> None:
    try:
        data = await state.get_data()

        if callback_query.data == "single_event_start_time":
            await state.set_state(NewEvent.start_time)
            await callback_query.message.answer(single_event_start_time_message)

        elif callback_query.data == "single_event_end_time":
            await state.set_state(NewEvent.end_time)
            await callback_query.message.answer(single_event_end_time_message)

        elif callback_query.data == "single_event_duration":
            await state.set_state(NewEvent.lesson_duration)
            await callback_query.message.answer(single_event_duration_message)

        elif callback_query.data == "single_event_breaks":
            await state.set_state(NewEvent.breaks)
            await callback_query.message.answer(single_event_breaks_message_unpack(data["breaks"] ,single_event_breaks_message)
                                                , reply_markup=single_event_breaks_keyboard)

        elif callback_query.data == "return_to_template_type":
            await state.set_state(NewEvent.type_of_schedule)
            await callback_query.message.answer(add_schedule_message, reply_markup=type_of_schedule_keyboard)

        elif callback_query.data == "confirm_single_template":
            if not validate_all_parameters(data):
                await callback_query.message.answer("Please fill in all the fields.")
                await state.set_state(NewEvent.single_template)

                await callback_query.message.answer(
                    single_template_message_unpack(
                        template=single_template_message,
                        data=data
                    ),
                    reply_markup=single_template_keyboard)

            else:
                start_time = data.get('start_time')
                end_time = data.get('end_time')
                lesson_duration = int(data.get('lesson_duration'))
                breaks = data.get('breaks')

                data_correctness, schedule = generate_schedule(start_time, end_time, lesson_duration, breaks)

                if not data_correctness:
                    await callback_query.message.answer(schedule)
                    return

                await state.update_data(final_schedule=schedule)
                await state.set_state(NewEvent.description)
                await callback_query.message.answer(created_schedule_message_unpack(created_schedule_message, schedule))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewEvent.start_time)
@restricted
async def add_start_time_handler(message: types.Message,
                                 state: FSMContext) -> None:
    try:
        start_time = message.text

        data_correctness, start_time_answer = validate_time(start_time)

        if not data_correctness:
            await message.answer(f"{start_time_answer}\n\nTry again using this format.")
            return

        await state.update_data(start_time=start_time_answer)

        await state.set_state(NewEvent.single_template)

        dates = await state.get_data()

        await message.answer(
            single_template_message_unpack(
                template=single_template_message,
                data=dates
            ),
            reply_markup=single_template_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewEvent.end_time)
@restricted
async def add_end_time_handler(message: types.Message,
                               state: FSMContext) -> None:
    try:
        end_time = message.text

        data_correctness, end_time_answer = validate_time(end_time)

        if not data_correctness:
            await message.answer(f"{end_time_answer}\n\nPlease try again.")
            return

        data = await state.get_data()
        start_time = data.get('start_time')

        if start_time and end_time_answer <= start_time:
            await message.answer("End time must be greater than start time. Please try again.")
            return

        await state.update_data(end_time=end_time_answer)

        await state.set_state(NewEvent.single_template)

        dates = await state.get_data()

        await message.answer(
            single_template_message_unpack(
                template=single_template_message,
                data=dates
            ),
            reply_markup=single_template_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewEvent.lesson_duration)
@restricted
async def add_lesson_duration_handler(message: types.Message,
                                      state: FSMContext) -> None:
    try:
        lesson_duration = message.text

        if not lesson_duration.isdigit() or int(lesson_duration) < 1:
            await message.answer("Invalid lesson duration. Please try again.")
            return

        await state.update_data(lesson_duration=lesson_duration)

        await state.set_state(NewEvent.single_template)

        dates = await state.get_data()

        await message.answer(
            single_template_message_unpack(
                template=single_template_message,
                data=dates
            ),
            reply_markup=single_template_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(NewEvent.breaks)
@restricted
async def add_breaks_handler(callback_query: types.CallbackQuery,
                             state: FSMContext) -> None:
    try:
        if callback_query.data == "add_break":
            await state.set_state(NewEvent.add_breaks)
            await callback_query.message.answer(single_event_add_breaks_message)

        elif callback_query.data == "return_to_breaks":
            await state.set_state(NewEvent.single_template)
            data = await state.get_data()
            await callback_query.message.answer(single_template_message_unpack(single_template_message, data),
                                                reply_markup=single_template_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewEvent.add_breaks)
@restricted
async def add_breaks_handler(message: types.Message,
                             state: FSMContext) -> None:
    try:
        break_time = message.text

        data_correctness, breaks_answer = validate_breaks(break_time)

        if not data_correctness:
            await message.answer(f"{breaks_answer}\n\nPlease try again.")
            return

        data = await state.get_data()
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time is None or end_time is None:
            await message.answer("Start time and end time must be set before adding breaks. Please try again.")
            await state.set_state(NewEvent.single_template)
            await message.answer(
                single_template_message_unpack(
                    template=single_template_message,
                    data=data
                ),
                reply_markup=single_template_keyboard)
            return

        start_time_dt = datetime.strptime(start_time, '%H:%M')
        end_time_dt = datetime.strptime(end_time, '%H:%M')

        new_break_start_str, new_break_end_str = break_time.split('-')
        new_break_start = datetime.strptime(new_break_start_str, '%H:%M')
        new_break_end = datetime.strptime(new_break_end_str, '%H:%M')

        if new_break_start < start_time_dt or new_break_end > end_time_dt:
            await message.answer("Break time must be within the start and end times. Please try again.")
            return

        if data["breaks"] is None:
            breaks = [break_time]
        else:
            breaks = data["breaks"]
            for existing_break in breaks:
                existing_break_start_str, existing_break_end_str = existing_break.split('-')
                existing_break_start = datetime.strptime(existing_break_start_str, '%H:%M')
                existing_break_end = datetime.strptime(existing_break_end_str, '%H:%M')

                if new_break_start < existing_break_end and new_break_end > existing_break_start:
                    await message.answer("Break times cannot overlap. Please try again.")
                    return

            breaks.append(break_time)

        await state.update_data(breaks=breaks)

        await state.set_state(NewEvent.single_template)

        data = await state.get_data()

        await message.answer(
            single_template_message_unpack(
                template=single_template_message,
                data=data
            ),
            reply_markup=single_template_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(NewEvent.description)
@restricted
async def add_description_handler(message: types.Message,
                                  state: FSMContext) -> None:
    try:
        description = message.text

        if len(description) > 1000:
            answer = await message.answer("The description is too long. Please try again.")
            return

        await state.update_data(description=description)

        data = await state.get_data()

        await add_event_with_schedule(data.get('dates'),
                                      data.get('name'),
                                      data.get('description'),
                                      data.get("dates")[0],
                                      data.get("dates")[-1],
                                      data.get('start_time'),
                                      data.get('end_time'),
                                      data.get('lesson_duration'),
                                      data.get('breaks'),
                                      data.get('final_schedule'),
                                      message.from_user.id)

        answer = await message.answer(single_event_created_message_unpack(event_created_message, data),
                                      reply_markup=start_keyboard)

        await state.clear()

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)