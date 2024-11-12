import re

from aiogram import F, Router, types
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext
from app.database.requests.coaches.add_coach import *
from app.keyboards.coaches.add_coach import *
from app.scripts.auxiliary_functions.delete_messages import (
    delete_previous_messages_bot,
    delete_previous_messages_user,
)
from app.scripts.coaches.add_coach import *
from app.states.coaches.add_coach import NewCoach
from app.templates.coaches.add_coach import *

# from app.keyboards.start.start import start_keyboard


router = Router()


@router.message(F.text == "Add new coach")
async def command_add_new_coach_handler(
    message: types.Message, bot: Bot, latest_messages: dict, state: FSMContext
) -> None:
    await state.clear()

    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    answer = await message.answer(add_coach_message, reply_markup=add_coach_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(F.text == "Add coach")
async def command_add_coach_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    await state.set_state(NewCoach.name)

    answer = await message.answer(
        add_name_message, reply_markup=types.ReplyKeyboardRemove()
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(NewCoach.name)
async def command_add_coach_name_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
        await message.answer("Please enter a valid Name")
        return

    await state.update_data(name=message.text)
    await state.set_state(NewCoach.surname)

    answer = await message.answer(add_surname_message)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(NewCoach.surname)
async def command_add_coach_surname_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    if not re.compile(r"^[a-zA-Z'-]+$").match(message.text):
        await message.answer("Please enter a valid Surname")
        return

    await state.update_data(surname=message.text)
    await state.set_state(NewCoach.program)

    answer = await message.answer(
        add_program_message, reply_markup=add_coach_program_keyboard
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(NewCoach.program)
async def command_create_new_event_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    if message.text not in ["Latin", "Ballroom"]:
        await message.answer("Please choose one of the options")
        return

    await state.update_data(program=True if message.text == "Latin" else False)

    dates_of_camp, full_schedule = await get_days_of_the_camp()

    await state.update_data(
        available_dates=dates_of_camp, choose_dates=[], full_schedule=full_schedule
    )

    keyboard = create_keyboard_for_dates(dates_of_camp)

    await state.set_state(NewCoach.selecting_numbers)

    answer = await message.answer(add_dates_message, reply_markup=keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.callback_query(NewCoach.selecting_numbers)
async def process_number_selection(
    callback_query: types.CallbackQuery, state: FSMContext
):
    data = await state.get_data()

    available_dates = data.get("available_dates", [])
    choose_dates = data.get("choose_dates", [])

    if callback_query.data.startswith("num_"):
        number = callback_query.data.split("_")[1]
        if number in available_dates:
            available_dates.remove(number)
            choose_dates.append(number)
            await state.update_data(
                avaible_dates=available_dates, choosen_dates=choose_dates
            )

    if callback_query.data == "confirm":
        await state.update_data(dates=choose_dates)
        await state.set_state(NewCoach.price)
        await callback_query.message.answer(add_price_message)
        return

    keyboard = create_keyboard_for_dates(available_dates)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)


@router.message(NewCoach.price)
async def command_create_new_event_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    price = message.text

    if not price.isdigit():
        await message.answer("Please enter a number")
        return

    await state.update_data(price=price)

    answer = await message.answer(
        add_currency_message, reply_markup=add_currency_keyboard
    )

    await state.set_state(NewCoach.currency)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )


@router.message(NewCoach.currency)
async def command_create_new_event_handler(
    message: types.Message, state: FSMContext, bot: Bot, latest_messages: dict
) -> None:
    await delete_previous_messages_bot(
        bot, message.chat.id, message.from_user.id, latest_messages
    )

    if message.text not in ["EUR", "USD", "UAH", "GBP"]:
        await message.answer("Please choose one of the options")
        return

    await state.update_data(currency=message.text)

    data = await state.get_data()

    await add_coach_to_db(data, data["full_schedule"])

    answer = await message.answer(
        await coach_added_message_unpack(data, coach_added_message),
        reply_markup=add_coach_keyboard,
    )

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)

    await state.clear()
    await delete_previous_messages_user(
        bot, message.chat.id, message.from_user.id, latest_messages
    )
