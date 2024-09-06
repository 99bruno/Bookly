from aiogram import types, Router, F
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext

from app.keyboards.edit_current_event.edit_current_event import edit_current_event_keyboard

from app.scripts.auxiliary_functions.delete_messages import delete_previous_messages_bot, delete_previous_messages_user

from app.templates.edit_current_event.edit_current_event import edit_current_event_message

router = Router()


@router.message(F.text == "Edit the current event")
async def command_edit_current_event_handler(message: types.Message,
                                             bot: Bot,
                                             latest_messages: dict,
                                             state: FSMContext) -> None:
    await state.clear()
    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    answer = await message.answer(edit_current_event_message, reply_markup=edit_current_event_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(F.text == "Back to menu")
async def command_edit_current_event_handler(message: types.Message,
                                             bot: Bot,
                                             latest_messages: dict,
                                             state: FSMContext) -> None:
    await state.clear()

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    answer = await message.answer(edit_current_event_message, reply_markup=edit_current_event_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)