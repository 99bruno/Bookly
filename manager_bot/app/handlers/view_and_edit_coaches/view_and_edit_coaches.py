import re

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from app.database.requests.view_and_edit_coaches.view_and_edit_coaches import *
from app.keyboards.view_and_edit_coaches.view_and_edit_coaches import *
from app.scripts.view_and_edit_coaches.view_and_edit_coaches import *
from app.states.view_and_edit_coaches.view_and_edit_coaches import *
from app.templates.view_and_edit_coaches.view_and_edit_coaches import *
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(F.text == "View and edit coaches")
async def view_and_edit_coaches_handler(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await state.clear()

        coaches_info = await get_all_coaches()

        await state.set_state(ListOfCoaches.coaches)
        await state.update_data(coaches_info=coaches_info)

        await message.answer(
            coaches_unpack_info(coaches_info, coaches_list_message),
            reply_markup=coaches_list_keyboard(coaches_info),
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda c: c.data == "return_to_coaches_menu")
async def callback_return_to_coaches_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        await state.clear()

        await callback_query.message.answer(
            coaches_message, reply_markup=coach_keyboard
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda c: c.data == "back_to_menu")
async def callback_return_to_coaches_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        await state.clear()

        await callback_query.message.answer(
            edit_current_event_message, reply_markup=edit_current_event_keyboard
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data.startswith("coach_"))
async def callback_coach_info_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        coach_number = int(callback_query.data.split("_")[1])

        await state.update_data(current_coach=coach_number)

        data = await state.get_data()

        coach_info = data["coaches_info"][coach_number]

        await callback_query.message.edit_text(
            coach_unpack_info(coach_info, coach_info_message)
        )
        await callback_query.message.edit_reply_markup(reply_markup=coach_info_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda c: c.data == "return_to_coaches")
async def callback_return_to_coaches_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        coaches = await state.get_data()

        await callback_query.message.edit_text(
            coaches_unpack_info(coaches["coaches_info"], coaches_list_message)
        )
        await callback_query.message.edit_reply_markup(
            reply_markup=coaches_list_keyboard(coaches["coaches_info"])
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda c: c.data == "edit_info")
async def callback_return_to_coaches_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        coaches = await state.get_data()
        coach_info = coaches["coaches_info"][coaches["current_coach"]]

        await state.set_state(ListOfCoaches.edit)

        await callback_query.message.edit_text(
            coach_unpack_info_for_edit(coach_info, coach_info_message)
        )
        await callback_query.message.edit_reply_markup(reply_markup=coach_edit_keyboard)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(ListOfCoaches.edit)
async def callback_return_to_coaches_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        if callback_query.data == "edit_coach_name":
            await state.set_state(ListOfCoaches.name)
            await callback_query.message.answer("Write correct name in chat 👇")

        elif callback_query.data == "edit_coach_surname":
            await state.set_state(ListOfCoaches.surname)
            await callback_query.message.answer("Write correct surname below 👇")

        elif callback_query.data == "edit_coach_program":
            await state.set_state(ListOfCoaches.program)
            await callback_query.message.edit_text(
                "Interesting changes! Choose another program 💃🏼"
            )
            await callback_query.message.edit_reply_markup(
                reply_markup=program_keyboard
            )

        elif callback_query.data == "edit_coach_price":
            await state.set_state(ListOfCoaches.price)
            await callback_query.message.answer("What would be the updated price? 💵")

        elif callback_query.data == "edit_coach_currency":
            await state.set_state(ListOfCoaches.currency)
            await callback_query.message.edit_text(
                "Choose the correct currency below 💸"
            )
            await callback_query.message.edit_reply_markup(
                reply_markup=currency_keyboard
            )

        elif callback_query.data == "lesson_restrictions":
            await state.set_state(ListOfCoaches.lesson_restrictions)
            await callback_query.message.answer(
                (
                    "<b>Set Lesson Limit 🎯</b>\n\n"
                    "Please specify the maximum number of "
                    "lessons a dance pair can book with a coach:"
                )
            )

        elif callback_query.data == "return_to_coach":
            coaches = await state.get_data()
            coach_info = coaches["coaches_info"][coaches["current_coach"]]

            await state.set_state(ListOfCoaches.coach)

            await callback_query.message.edit_text(
                coach_unpack_info(coach_info, coach_info_message)
            )
            await callback_query.message.edit_reply_markup(
                reply_markup=coach_info_keyboard
            )

        elif callback_query.data == "back_to_menu":
            await state.clear()
            await callback_query.message.answer(
                edit_current_event_message, reply_markup=edit_current_event_keyboard
            )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(ListOfCoaches.name)
async def edit_coach_name_handler(message: types.Message, state: FSMContext) -> None:
    try:
        coach_name = message.text

        if not re.compile(r"^[a-zA-Z'-]+$").match(coach_name):
            await message.answer("Please enter a valid Name")
            return

        coach_info = await state.get_data()

        await update_coach_info(
            coach_info["coaches_info"][coach_info["current_coach"]]["id"],
            "firstname",
            coach_name,
        )

        coach_info["coaches_info"][coach_info["current_coach"]]["name"] = coach_name

        surname = coach_info["coaches_info"][coach_info["current_coach"]]["surname"]

        coach_info["coaches_info"][coach_info["current_coach"]]["coach"] = (
            coach_name + " " + surname
        )

        await state.update_data(coaches_info=coach_info["coaches_info"])

        await message.answer("Coach name has been updated")

        await state.set_state(ListOfCoaches.edit)
        await message.answer(
            coach_unpack_info(
                coach_info["coaches_info"][coach_info["current_coach"]],
                coach_info_message,
            ),
            reply_markup=coach_info_keyboard,
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(ListOfCoaches.surname)
async def edit_coach_surname_handler(message: types.Message, state: FSMContext) -> None:
    try:
        coach_surname = message.text
        if not re.compile(r"^[a-zA-Z'-]+$").match(coach_surname):
            await message.answer("Please enter a valid Surname")
            return

        coach_info = await state.get_data()

        await update_coach_info(
            coach_info["coaches_info"][coach_info["current_coach"]]["id"],
            "lastname",
            coach_surname,
        )

        coach_info["coaches_info"][coach_info["current_coach"]][
            "surname"
        ] = coach_surname

        name = coach_info["coaches_info"][coach_info["current_coach"]]["name"]

        coach_info["coaches_info"][coach_info["current_coach"]]["coach"] = (
            name + " " + coach_surname
        )

        await state.update_data(coaches_info=coach_info["coaches_info"])

        await callback_query.answer("Coach surname has been updated", show_alert=True)

        await state.set_state(ListOfCoaches.edit)
        await message.answer(
            coach_unpack_info(
                coach_info["coaches_info"][coach_info["current_coach"]],
                coach_info_message,
            ),
            reply_markup=coach_info_keyboard,
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda c: c.data == "latin" or c.data == "ballroom")
async def edit_coach_program_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        coach_program = True if callback_query.data == "latin" else False

        coach_info = await state.get_data()

        await update_coach_info(
            coach_info["coaches_info"][coach_info["current_coach"]]["id"],
            "program",
            coach_program,
        )

        coach_info["coaches_info"][coach_info["current_coach"]][
            "program"
        ] = coach_program

        await state.update_data(coaches_info=coach_info["coaches_info"])

        await callback_query.message.answer("Coach program has been updated")
        await state.set_state(ListOfCoaches.edit)
        await callback_query.message.answer(
            coach_unpack_info(
                coach_info["coaches_info"][coach_info["current_coach"]],
                coach_info_message,
            ),
            reply_markup=coach_info_keyboard,
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(ListOfCoaches.price)
async def edit_coach_price_handler(message: types.Message, state: FSMContext) -> None:
    try:
        coach_price = message.text
        if not coach_price.isdigit():
            await message.answer("Price can't be empty or contain letters")
            return

        coach_info = await state.get_data()

        await update_coach_info(
            coach_info["coaches_info"][coach_info["current_coach"]]["id"],
            "price",
            coach_price,
        )

        coach_info["coaches_info"][coach_info["current_coach"]]["price"] = coach_price

        await state.update_data(coaches_info=coach_info["coaches_info"])

        await message.answer("Coach price has been updated", show_alert=True)
        await state.set_state(ListOfCoaches.edit)
        await message.answer(
            coach_unpack_info(
                coach_info["coaches_info"][coach_info["current_coach"]],
                coach_info_message,
            ),
            reply_markup=coach_info_keyboard,
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(
    lambda c: c.data == "USD" or c.data == "EUR" or c.data == "UAH" or c.data == "GBP"
)
async def edit_coach_currency_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        data = callback_query.data
        id_currency = currency.index(data) + 1

        coach_info = await state.get_data()

        await update_coach_info(
            coach_info["coaches_info"][coach_info["current_coach"]]["id"],
            "currency",
            id_currency,
        )

        coach_info["coaches_info"][coach_info["current_coach"]][
            "currency"
        ] = id_currency

        await state.update_data(coaches_info=coach_info["coaches_info"])

        await callback_query.message.answer("Coach price currency has been updated")

        await state.set_state(ListOfCoaches.edit)
        await callback_query.message.answer(
            coach_unpack_info(
                coach_info["coaches_info"][coach_info["current_coach"]],
                coach_info_message,
            ),
            reply_markup=coach_info_keyboard,
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(ListOfCoaches.lesson_restrictions)
async def edit_coach_price_handler(message: types.Message, state: FSMContext) -> None:
    try:
        if not message.text.isdigit():
            await message.answer("Please enter a valid number")
            return

        lesson_restrictions = message.text

        coach_info = await state.get_data()

        await update_coach_info(
            coach_info["coaches_info"][coach_info["current_coach"]]["id"],
            "lesson_restrictions",
            lesson_restrictions,
        )

        coach_info["coaches_info"][coach_info["current_coach"]][
            "lesson_restrictions"
        ] = lesson_restrictions

        await state.update_data(coaches_info=coach_info["coaches_info"])

        await message.answer("Coach lesson restrictions has been updated")

        await state.set_state(ListOfCoaches.edit)
        await message.answer(
            coach_unpack_info(
                coach_info["coaches_info"][coach_info["current_coach"]],
                coach_info_message,
            ),
            reply_markup=coach_info_keyboard,
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda c: c.data == "view_schedule")
async def callback_return_to_coaches_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        data = await state.get_data()

        await state.set_state(ListOfCoaches.current_date)

        await callback_query.message.edit_reply_markup(
            reply_markup=create_keyboard_for_dates(
                data["coaches_info"][data["current_coach"]]["dates"]
            )
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(ListOfCoaches.current_date)
async def callback_view_schedule_handler(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    try:
        if callback_query.data == "return_to_coach_info":
            data = await state.get_data()
            await state.set_state(ListOfCoaches.coach)

            await callback_query.message.edit_text(
                coach_unpack_info(
                    data["coaches_info"][data["current_coach"]], coach_info_message
                )
            )

            await callback_query.message.edit_reply_markup(
                reply_markup=coach_info_keyboard
            )
            return

        elif callback_query.data.startswith("date_"):
            data = await state.get_data()
            date_ = callback_query.data.split("_")[-1].split(".")

            schedule_info = await view_coach_schedule(
                data["coaches_info"][data["current_coach"]]["id"],
                datetime.date(int(date_[2]), int(date_[1]), int(date_[0])),
            )

            await callback_query.message.edit_text(
                coach_view_schedule_unpack(
                    [callback_query.data.split("_")[-1], schedule_info, data["coaches_info"][data["current_coach"]]["coach"]],
                    coach_view_schedule_message,
                )
            )
            await callback_query.message.edit_reply_markup(
                reply_markup=create_keyboard_for_dates(
                    data["coaches_info"][data["current_coach"]]["dates"]
                )
            )
            return

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)
