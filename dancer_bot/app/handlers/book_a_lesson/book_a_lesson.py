from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from app.database.requests.book_a_lesson.book_a_lesson import *
from app.database.requests.book_a_lesson.check_dancer import check_user_registered, check_couple_registered

from app.keyboards.book_a_lesson.book_a_lesson import *
from app.keyboards.start.start import start_keyboard

from app.scripts.auxiliary_functions.format_strings import format_string
from app.scripts.book_a_lesson.book_a_lesson import concatenate_couples, format_couple, format_lesson_info

from app.states.book_a_lesson.book_a_lesson import LessonRegistration
from app.states.book_a_lesson.register_dancer import UserRegistration

from app.templates.book_a_lesson.book_a_lesson import *

router = Router()


@router.message(F.text == "Забронювати уроки 📅")
async def command_book_a_lesson_handler(message: types.Message, state: FSMContext) -> None:
    await state.clear()

    user_info = await check_user_registered(message.from_user.id)
    if user_info:
        couple_info = await check_couple_registered(user_info)
        if couple_info:

            await state.set_state(LessonRegistration.couples)
            await state.update_data(couples=couple_info)

            couples = concatenate_couples(couple_info)

            await message.answer(format_string(choose_couple_message, ["\n".join(format_couple(couples))]),
                                 reply_markup=create_keyboard_for_choose_couple(couples))
        else:
            await message.answer(register_couple_message, reply_markup=change_partner_solo_or_couple_keyboard)
    else:
        await state.set_state(UserRegistration.phone_number)
        await message.answer(enter_phone_number_message, reply_markup=share_contact_keyboard)


@router.callback_query(lambda c: c.data == 'change_couple')
async def handle_change_couple(callback_query: types.CallbackQuery) -> None:
    await callback_query.message.answer(change_partner_solo_or_couple_message,
                                        reply_markup=change_partner_solo_or_couple_keyboard)


@router.callback_query(lambda event: event.data.startswith('couple_'))
async def handle_couple_selection(callback_query: types.CallbackQuery,
                                  state: FSMContext) -> None:
    couple_id = callback_query.data.split('_')[-1]

    await state.set_state(LessonRegistration.couple_id)
    await state.update_data(couple_id=couple_id)
    data = await state.get_data()
    await state.set_state(LessonRegistration.program)

    await callback_query.message.answer(format_string(choose_program_message,
                                                      concatenate_couples([data["couples"][int(couple_id)]])),
                                        reply_markup=choose_program_keyboard)


@router.message(LessonRegistration.program)
async def handle_program_selection(message: types.Message,
                                   state: FSMContext) -> None:
    program = message.text

    await state.update_data(program=program)
    coaches = await get_coaches_by_program(program)
    await state.update_data(coaches=coaches)
    await state.set_state(LessonRegistration.coach_id)

    await message.answer(available_dates_message, reply_markup=create_keyboard_for_coaches(coaches))


@router.callback_query(lambda event: event.data.startswith('coach_'))
async def handle_coach_selection(callback_query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    coach_id = int(callback_query.data.split('_')[-1])
    data = await state.get_data()

    dates = await get_lessons_by_coach(coach_id, data["couples"][int(data["couple_id"])]["couple_id"])

    await state.update_data(coach_id=coach_id)
    await state.update_data(all_dates=dates)
    await state.update_data(available_dates=list(dates.keys()))
    await state.set_state(LessonRegistration.selected_dates)

    await callback_query.message.answer_photo(photo=FSInputFile("app/database/Unknown.jpeg"),
                                              reply_markup=create_keyboard_for_dates(list(dates.keys())),
                                              caption="Яка дата тебе цікавить? "
                                              )


@router.callback_query(LessonRegistration.selected_dates)
async def process_number_selection(callback_query: types.CallbackQuery,
                                   state: FSMContext):
    data = await state.get_data()

    choose_dates = data.get('choose_dates', [])
    all_dates = data.get('all_dates', [])
    available_dates = data.get('available_dates', [])
    current_date = data.get('current_date', None)

    if callback_query.data.startswith('date_'):
        date_id = int(callback_query.data.split('_')[-1])
        date = available_dates[date_id]

        await state.update_data(current_date=date)

        await callback_query.message.edit_caption(caption="Тепер обери зручний для тебе час 🤩\n\n"
                                                          "Ти можеш обрати одразу кілька занять, "
                                                          "клікнувши на декілька кнопок. "
                                                          "Максимальна кількість занять з одним тренером/-кою - 4. "
                                                          "Якщо тобі потрібно забронювати більше уроків, то, "
                                                          "будь ласка, звернися до менеджера 🫂")

        await callback_query.message.edit_reply_markup(
            reply_markup=create_keyboard_for_time(list(all_dates[date].keys())))

    if callback_query.data.startswith('time_'):
        time_id = callback_query.data.split('_')[-1]
        choose_dates.append(all_dates[current_date][time_id])

        all_dates[current_date].pop(time_id)
        await state.update_data(all_dates=all_dates, choose_dates=choose_dates)
        keyboard = create_keyboard_for_time(all_dates[current_date])

        await callback_query.message.edit_reply_markup(reply_markup=keyboard)

    if callback_query.data == 'return_to_dates':
        keyboard = create_keyboard_for_dates(available_dates)

        await callback_query.message.edit_caption(caption="Яка дата тебе цікавить?")
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)

    if callback_query.data == 'book_lesson':
        await state.update_data(selected_dates=choose_dates)
        data_of_lessons = await get_lessons_info(choose_dates)

        await callback_query.message.answer(format_lesson_info(data_of_lessons, confirm_book_lessons_message),
                                            reply_markup=confirm_book_lessons_keyboard)

        await state.set_state(LessonRegistration.confirmation)


@router.callback_query(lambda event: event.data == 'lesson_booking_confirmation')
async def command_book_lessons_handler(callback_query: types.CallbackQuery,
                                       state: FSMContext) -> None:
    data = await state.get_data()

    unavailable_lessons = await book_lessons(data["selected_dates"],
                                             data["couples"][int(data["couple_id"])]["couple_id"],
                                             data["coach_id"])

    await state.clear()

    if unavailable_lessons:
        await callback_query.answer(unavailable_lessons_message.format(", ".join(unavailable_lessons)),
                                    show_alert=True)

    await callback_query.message.answer(confirmed_book_lessons_message, reply_markup=start_keyboard)
