from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from app.database.requests.settings.add_manager import *
from app.keyboards.settings.managers import *
from app.scripts.settings.managers import remove_managers_msg_unpack
from app.scripts.settings.settings import restricted
from app.states.settings.managers import ManagerEdit
from app.templates.settings.managers import *
from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.message(F.text == "Edit managers")
@restricted
async def edit_managers_handler(message: types.Message, state: FSMContext):
    try:
        await message.answer(managers_msg, reply_markup=managers_kb)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Add manager")
@restricted
async def add_manager_handler(message: types.Message, state: FSMContext):
    try:
        await state.set_state(ManagerEdit.add_manager)

        await message.answer(add_manager_msg, reply_markup=types.ReplyKeyboardRemove())

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(ManagerEdit.add_manager)
@restricted
async def added_manager_handler(message: types.Message, state: FSMContext):
    try:
        await add_manager(int(message.text.split()[0]), message.text.split()[1])

        await message.answer(added_manager_msg, reply_markup=managers_kb)

        await state.clear()

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Add admin")
@restricted
async def add_admin_handler(message: types.Message, state: FSMContext):
    try:
        await state.set_state(ManagerEdit.add_admin)

        await message.answer(add_manager_msg, reply_markup=types.ReplyKeyboardRemove())

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(ManagerEdit.add_admin)
@restricted
async def added_manager_handler(message: types.Message, state: FSMContext):
    try:
        await add_admin(int(message.text.split()[0]), message.text.split()[1])

        await message.answer(added_admin_msg, reply_markup=managers_kb)

        await state.clear()

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Remove manager")
@restricted
async def remove_manager_handler(message: types.Message, state: FSMContext):
    try:
        await message.answer(
            await remove_managers_msg_unpack(
                managers := await get_managers(), remove_managers_msg
            ),
            reply_markup=await remove_manager_kb(managers),
        )

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda query: query.data.startswith("manager"))
@restricted
async def remove_manager_handler(query: types.CallbackQuery, state: FSMContext):
    await remove_manager(int(query.data.split("_")[1]))
    await query.message.answer("Manager has been removed", reply_markup=managers_kb)
    """except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", query.from_user.id)
            scope.set_extra("username", query.from_user.username)
        sentry_sdk.capture_exception(e)"""
