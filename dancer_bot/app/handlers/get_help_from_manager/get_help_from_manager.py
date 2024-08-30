from aiogram import types, html, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


from app.keyboards.start.start import back_to_main_menu_keyboard

from app.templates.get_help_from_manager.get_help_from_manager import get_help_from_manager_message


router = Router()

@router.message(F.text == "Потрібна допомога? 🆘")
async def command_check_camp_info_handler(message: types.Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(get_help_from_manager_message, reply_markup=back_to_main_menu_keyboard)