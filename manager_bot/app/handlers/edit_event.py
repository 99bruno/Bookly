from aiogram import types, html, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.client.bot import Bot

from app.keyboards.edit_event import *

from app.templates.edit_event import *

from app.scripts.auxiliary_functions.get_days_between_dates import get_days_of_the_camp
from app.scripts.auxiliary_functions.check_access import check_access
from app.scripts.edit_event.edit_event import edit_camp_info
from app.scripts.auxiliary_functions.format_strings import format_string
from app.scripts.auxiliary_functions.delete_messages import delete_previous_messages_bot, delete_previous_messages_user

from app.database.requests.edit_event import get_event_info


router = Router()


class NewCoach(StatesGroup):
    name = State()
    surname = State()
    price = State()
    program = State()
    dates = State()


class Event(StatesGroup):
    name = State()
    date = State()
    description = State()


@router.message(F.text == "Edit the current event")
async def command_edit_current_event_handler(message: types.Message,
                                             bot: Bot,
                                             latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    answer = await check_access(message, edit_event_message, edit_event_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(F.text == "Back to menu")
async def command_back_to_menu_handler(message: types.Message,
                                       bot: Bot,
                                       latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    answer = await check_access(message, edit_event_message, edit_event_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(F.text == "View full schedule")
async def command_view_full_schedule_handler(message: types.Message,
                                             bot: Bot,
                                             latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    answer = await check_access(message, view_schedule_message, view_schedule_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(F.text == "Edit camp info")
async def command_create_new_event_handler(message: types.Message,
                                           bot: Bot,
                                           latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    event_info = await get_event_info()

    answer = await check_access(message,
                                format_string(edit_camp_info_message,
                                              [
                                                  event_info.name,
                                                  event_info.description if event_info.description != "" else " ",
                                                  event_info.date_start,
                                                  event_info.date_end,
                                              ]
                                              ),
                                edit_camp_info_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(F.text == "Change name of the camp")
async def command_create_new_event_handler(message: types.Message,
                                           state: FSMContext,
                                           bot: Bot,
                                           latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    await state.set_state(Event.name)

    answer = await check_access(message, change_name_message, types.ReplyKeyboardRemove())

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(Event.name)
async def command_add_event_name(message: types.Message,
                                 state: FSMContext,
                                 bot: Bot,
                                 latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    await state.update_data(name=message.text)
    data = await state.get_data()

    answer = await check_access(message, format_string(changed_name_message, list(data.values())), change_name_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await edit_camp_info(data)
    await state.clear()

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(F.text == "Change dates")
async def command_create_new_event_handler(message: types.Message,
                                           state: FSMContext,
                                           bot: Bot,
                                           latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    await state.set_state(Event.date)

    answer = await check_access(message, change_date_massage, types.ReplyKeyboardRemove())

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(Event.date)
async def command_add_event_name(message: types.Message,
                                 state: FSMContext,
                                 bot: Bot,
                                 latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    await state.update_data(date=message.text)
    data = await state.get_data()

    answer = await check_access(message, format_string(changed_date_massage, list(data.values())), change_date_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await edit_camp_info(data)

    await state.clear()

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(F.text == "Edit massage with full info")
async def command_create_new_event_handler(message: types.Message,
                                           state: FSMContext,
                                           bot: Bot,
                                           latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    await state.set_state(Event.description)

    event_info = await get_event_info()

    answer = await check_access(message,
                                format_string(change_description_massage,
                                              [event_info.description] if event_info else ["The event not exist"]),
                                types.ReplyKeyboardRemove())

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(Event.description)
async def command_add_event_name(message: types.Message,
                                 state: FSMContext,
                                 bot: Bot,
                                 latest_messages: dict) -> None:

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    await state.update_data(description=message.text)
    data = await state.get_data()

    answer = await check_access(message, changed_description_massage, change_description_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await edit_camp_info(data)

    await state.clear()

    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)