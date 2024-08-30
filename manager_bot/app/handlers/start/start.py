from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext

from app.keyboards.start.start import start_keyboard

from app.scripts.auxiliary_functions.delete_messages import delete_previous_messages_bot, delete_previous_messages_user

from app.templates.start.start import start_message, back_main_menu_message

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: types.Message,
                                bot: Bot,
                                latest_messages: dict,
                                state: FSMContext) -> None:
    await state.clear()

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    answer = await message.answer(start_message, reply_markup=start_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(F.text == "Back to the main menu")
async def command_back_to_main_menu_handler(message: types.Message,
                                            bot: Bot,
                                            latest_messages: dict,
                                            state: FSMContext) -> None:
    await state.clear()

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    answer = await message.answer(back_main_menu_message, reply_markup=start_keyboard)

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)
