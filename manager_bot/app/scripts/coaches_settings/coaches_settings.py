from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(F.text == "Coaches settings")
async def coaches_settings_handler(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        await message.answer(start_message_1)
        await message.answer(start_message_2, reply_markup=start_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
