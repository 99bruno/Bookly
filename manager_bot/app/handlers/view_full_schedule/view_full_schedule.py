from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from app.database.requests.view_full_schedule.view_schedule import *
from app.templates.view_full_schedule.view_full_schedule import *
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(F.text == "View full schedule")
async def command_view_full_schedule_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.clear()

        await fetch_lessons_with_full_info()

        await message.answer_document(
            FSInputFile("app/database/schedule.xlsx"), caption=view_schedule_message
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)
