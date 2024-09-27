from aiogram import types, html, F, Router
from aiogram.fsm.context import FSMContext

from app.templates.check_camp_info.check_camp_info import *

from app.keyboards.check_camp_info.check_camp_info import *

from app.database.requests.get_help_from_manager.get_help_from_manager import get_event_info
from app.database.requests.check_camp_info.check_camp_info import *

from app.scripts.auxiliary_functions.format_strings import format_string
from app.scripts.check_camp_info.check_camp_info import *

from app.states.check_camp_info.check_camp_info import Coach

from sentry_logging.sentry_setup import sentry_sdk


router = Router()


@router.message(F.text == "Інформація про кемп 🪩")
async def command_check_camp_info_handler(message: types.Message, state: FSMContext) -> None:
    try:
        await state.clear()

        event_info = await get_event_info()

        await message.answer(await check_camp_info_message_unpack([
                                                      event_info.name,
                                                      event_info.date_start,
                                                      event_info.date_end,
                                                      event_info.description
                                                  ], check_camp_info_message), reply_markup=check_camp_info_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)



@router.callback_query(lambda query: query.data == "return_to_check_camp_info")
async def command_check_camp_info_handler(query: types.CallbackQuery) -> None:
    try:
        event_info = await get_event_info()

        await query.message.answer(format_string(check_camp_info_message, [
                                                      event_info.name,
                                                      event_info.date_start,
                                                      event_info.date_end,
                                                      event_info.description
                                                  ]), reply_markup=check_camp_info_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Тренери та ціни")
async def command_coaches_list_handler(message: types.Message) -> None:
    try:

        await message.answer(coaches_program_choose_message,
                             reply_markup=coaches_program_choose_keyboard)
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda query: query.data.startswith("coaches_program_choose"))
async def command_coaches_list_handler(query: types.CallbackQuery,
                                       state: FSMContext) -> None:
    try:
        program = await get_coaches_by_program(query.data.split("_")[-1])

        await state.update_data(program=query.data.split("_")[-1])

        await query.message.edit_text(await coaches_list_message_unpack(program, coaches_list_message))
        await query.message.edit_reply_markup(reply_markup=create_keyboard_for_coaches_camp_info(program))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda query: query.data == "return_to_program_choose")
async def command_coaches_list_handler(query: types.CallbackQuery) -> None:
    try:

        await query.message.edit_text(coaches_program_choose_message)
        await query.message.edit_reply_markup(reply_markup=coaches_program_choose_keyboard)
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda query: query.data == "return_to_coaches_list")
async def command_coaches_list_handler(query: types.CallbackQuery,
                                       state: FSMContext) -> None:
    try:
        data = await state.get_data()

        coaches = await get_coaches_by_program(data.get("program"))

        await query.message.edit_text(await coaches_list_message_unpack(coaches, coaches_list_message))
        await query.message.edit_reply_markup(reply_markup=create_keyboard_for_coaches_camp_info(coaches))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda query: query.data.startswith("camp_info_coach"))
async def coach_from_camp_info_handler(query: types.CallbackQuery,
                                       state: FSMContext) -> None:
    try:

        coach = await get_coach_info(int(query.data.split("_")[-1]))

        await state.update_data(coach_info=coach)

        await query.message.edit_text(await coach_info_message_unpack(coach, coach_info_message))
        await query.message.edit_reply_markup(reply_markup=coach_info_keyboard)
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda query: query.data == "view_price")
async def coach_from_camp_info_handler(query: types.CallbackQuery,
                                       state: FSMContext) -> None:
    try:
        data = await state.get_data()

        if await check_user_registered(query.from_user.id) is False:
            await query.message.edit_text(user_not_registered_message)
            await query.message.edit_reply_markup(reply_markup=coach_info_keyboard)
            return

        await query.message.edit_text(await coach_info_view_price_message_unpack(data.get("coach_info"),
                                                                              coach_info_view_price_message)
                                   )
        await query.message.edit_reply_markup(reply_markup=coach_view_price_keyboard)
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda query: query.data == "compare_prices")
async def coach_from_camp_info_handler(query: types.CallbackQuery,
                                       state: FSMContext) -> None:
    try:
        data = await state.get_data()

        coaches = await get_coaches_by_program(data.get("program"))

        await query.message.edit_text(await coach_info_compare_price_message_unpack(coaches,
                                                                                    coach_info_compare_price_message,
                                                                                    data.get("program")
                                                                                    ))

        await query.message.edit_reply_markup(reply_markup=create_keyboard_for_coaches_camp_info(coaches))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)

        sentry_sdk.capture_exception(e)
