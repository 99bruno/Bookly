import re

from aiogram import F, Router, html, types
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from app.database.requests.camp_info.edit_camp_info import *
from app.database.requests.camp_info.view_schedule import *
from app.keyboards.camp_info.edit_camp_info import *
from app.scripts.auxiliary_functions.delete_messages import (
    delete_previous_messages_bot,
    delete_previous_messages_user,
)
from app.scripts.camp_info.edit_camp_info import *
from app.states.camp_info.edit_camp_info import *
from app.templates.camp_info.edit_camp_info import *

router = Router()


@router.message(F.text == "Edit camp info")
async def command_edit_camp_info_handler(
    message: types.Message, bot: Bot, latest_messages: dict, state: FSMContext
) -> None:
    await state.clear()

    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    answer = await message.answer(
        await edit_event_message_unpack(await get_event_info(), edit_event_message),
        reply_markup=edit_event_keyboard,
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(F.text == "Change name of the camp")
async def command_create_new_event_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    await state.set_state(EditEvent.name)

    answer = await message.answer(
        change_name_message, reply_markup=types.ReplyKeyboardRemove()
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(EditEvent.name)
async def command_add_event_name(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    name = message.text

    if len(name) > 50 or not re.compile(r"^[a-zA-Z\s'-]+$").match(name):
        answer = await message.answer(
            "The name is too long or contains invalid characters. Please try again."
        )
        latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
        return

    await state.update_data(name=name)
    data = await state.get_data()
    await update_event(data)
    await state.clear()

    answer = await message.answer(
        await format_string(name, changed_name_message),
        reply_markup=change_name_keyboard,
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(F.text == "Edit massage with full info")
async def command_create_new_event_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    await state.set_state(EditEvent.description)

    data = await get_event_info()

    answer = await message.answer(
        await format_string([data.description], change_description_massage),
        reply_markup=types.ReplyKeyboardRemove(),
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(EditEvent.description)
async def command_add_event_name(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    description = message.text

    if len(description) > 1000:
        answer = await message.answer("The description is too long. Please try again.")
        latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
        return

    await state.update_data(description=message.text)
    data = await state.get_data()
    await update_event(data)
    await state.clear()

    answer = await message.answer(
        await format_string(description, changed_description_massage),
        reply_markup=change_description_keyboard,
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(F.text == "Change dates")
async def command_create_new_event_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    await state.set_state(EditEvent.date)

    answer = await message.answer(
        change_date_massage, reply_markup=types.ReplyKeyboardRemove()
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(EditEvent.date)
async def command_add_event_name(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    # data_correctness, date_answer = validate_date_range(message.text)

    """if not data_correctness:
        answer = await message.answer(f"{date_answer}\n\nPlease try again.")
        latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
        return

    await state.update_data(date=message.text)
    data = await state.get_data()
    await update_event(data)
    await state.clear()"""

    answer = await message.answer(
        "Oopppsss.. Now this function is not available currently 😕\n\n"
        "Please, contact support if you need help to change dates.",
        reply_markup=change_date_keyboard,
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )
    await state.clear()


@router.message(F.text == "View full schedule")
async def command_view_full_schedule_handler(
    message: types.Message, bot: Bot, latest_messages: dict, state: FSMContext
) -> None:
    await state.clear()

    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    await fetch_lessons_with_full_info()

    await message.answer_document(
        FSInputFile("schedule.xlsx"),
        caption=view_schedule_message,
        reply_markup=view_schedule_keyboard,
    )
