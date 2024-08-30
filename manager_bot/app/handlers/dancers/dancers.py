import re

from aiogram import types, Router, F
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext

from app.keyboards.dancers.dancers import *
from app.keyboards.edit_current_event.edit_current_event import edit_current_event_keyboard


from app.scripts.auxiliary_functions.delete_messages import delete_previous_messages_bot, delete_previous_messages_user
from app.scripts.dancers.dancers import *

from app.templates.dancers.dancers import *

from app.database.requests.dancers.dancers import *

from app.states.dancers.dancers import Dancers

router = Router()


@router.message(F.text == "Dancers info")
async def dancers_info(message: types.Message,
                       state: FSMContext,
                       bot: Bot,
                       latest_messages: dict) -> None:
    await state.clear()

    await delete_previous_messages_bot(bot, message.chat.id, message.from_user.id, latest_messages)

    await state.set_state(Dancers.dancers_info)

    answer = await message.answer(dancers_info_message, reply_markup=types.ReplyKeyboardRemove())

    latest_messages[message.from_user.id] = (answer.message_id, message.message_id)
    await delete_previous_messages_user(bot, message.chat.id, message.from_user.id, latest_messages)


@router.message(Dancers.dancers_info)
async def dancers_search(message: types.Message,
                         state: FSMContext) -> None:

    dancer_info = message.text

    phone = "".join(message.text.split())[1:] if message.text.startswith("+") else "".join(message.text.split())
    print(phone)

    if phone.isdigit() and len(phone) == 12:
        search_type = "phone"
        dancer_info = phone
    elif re.compile(r"^[a-zA-Z\s'-]+$").match(dancer_info):
        search_type = "name"
    else:
        await message.answer(dancer_not_found_message)
        return

    dancers = await search_dancers(dancer_info, search_type)

    if dancers:
        await state.update_data(dancers_info=dancers)

        await message.answer(await dancers_list_message_unpack(dancers, dancers_list_message), reply_markup=create_keyboard_for_dancers(dancers))
    else:
        await message.answer("No matching dancers found.")


@router.callback_query(F.data.startswith("dancer_"))
async def dancer_info(callback_query: types.CallbackQuery,
                      state: FSMContext) -> None:

    data = await state.get_data()

    dancers = data.get("dancers_info")
    dancer_id = int(callback_query.data.split("_")[1])

    dancer = dancers[dancer_id]

    await state.update_data(current__dancer=dancer_id)

    couples = await search_couples_by_dancer(dancer["id"])

    await callback_query.message.answer(await dancer_info_message_unpack(dancer, dancer_info_message, couples),
                                        reply_markup=create_keyboard_for_couples(couples))

    await state.update_data(couples_info=couples)


@router.callback_query(F.data == "return_to_dancers")
async def return_to_dancers(callback_query: types.CallbackQuery,
                            state: FSMContext) -> None:

    data = await state.get_data()
    dancers = data.get("dancers_info")


    await callback_query.message.edit_text(await dancers_list_message_unpack(dancers, dancers_list_message))
    await callback_query.message.edit_reply_markup(reply_markup=create_keyboard_for_dancers(dancers))


@router.callback_query(F.data.startswith("couple_"))
async def couple_info(callback_query: types.CallbackQuery,
                      state: FSMContext) -> None:

    data = await state.get_data()

    couples = data.get("couples_info")
    couple_id = int(callback_query.data.split("_")[1])

    couple = couples[couple_id]

    schedule = await get_booked_lessons_for_couple(couple["couple_id"])

    await state.update_data(lessons=schedule)

    await callback_query.message.edit_text(await couple_info_message_unpack(couple, couple_info_message, schedule))
    await callback_query.message.edit_reply_markup(reply_markup=couple_schedule_keyboard)


@router.callback_query(F.data == "return_to_couple")
async def return_to_couple(callback_query: types.CallbackQuery,
                           state: FSMContext) -> None:

    data = await state.get_data()
    couples = data.get("couples_info")
    current__dancer = data.get("current__dancer")
    dancers = data.get("dancers_info")
    dancer = dancers[current__dancer]

    await callback_query.message.edit_text(await dancer_info_message_unpack(dancer, dancer_info_message, couples))
    await callback_query.message.edit_reply_markup(reply_markup=create_keyboard_for_couples(couples))


@router.callback_query(F.data == "pay_all")
async def pay_all(callback_query: types.CallbackQuery,
                  state: FSMContext) -> None:

    await callback_query.message.edit_text(couple_schedule_paid_confirm_message)
    await callback_query.message.edit_reply_markup(reply_markup=couple_schedule_paid_confirm_keyboard)

    data = await state.get_data()
    lessons = data.get("lessons")

    await state.update_data(lessons_to_pay=[int(lesson["booked_lesson_id"]) for lesson in lessons])


@router.callback_query(F.data == "pay_selected")
async def pay_all(callback_query: types.CallbackQuery,
                  state: FSMContext) -> None:

    data = await state.get_data()
    lessons = data.get("lessons")

    await state.set_state(Dancers.select_lessons)

    available_lessons_to_pay = await sort_lessons(lessons)

    await state.update_data(available_lessons_to_pay=available_lessons_to_pay)

    await callback_query.message.edit_reply_markup(reply_markup=create_keyboard_for_lessons(available_lessons_to_pay))


@router.callback_query(Dancers.select_lessons)
async def process_number_selection(callback_query: types.CallbackQuery,
                                   state: FSMContext):

    data = await state.get_data()

    available_lessons = data.get('available_lessons_to_pay')
    choose_lessons = data.get('lessons_to_pay', [])

    if callback_query.data.startswith('lesson_'):
        lesson = available_lessons[callback_query.data.split('_')[1]]

        if lesson in available_lessons.values():
            available_lessons.pop(callback_query.data.split('_')[1])
            choose_lessons.append(int(lesson))
            await state.update_data(available_lessons_to_pay=available_lessons, lessons_to_pay=choose_lessons)

    if callback_query.data == 'confirm_payment_selected':
        await mark_lessons_as_paid(choose_lessons)
        await callback_query.message.answer(payment_confirmed_message, reply_markup=edit_current_event_keyboard)
        await state.clear()
        return

    keyboard = create_keyboard_for_lessons(available_lessons)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)



@router.callback_query(F.data.startswith("lesson_"))
async def select_lesson_to_pay(callback_query: types.CallbackQuery,
                               state: FSMContext) -> None:

    data = await state.get_data()
    lessons = data.get("lessons_all")

    lesson_id = int(callback_query.data.split("_")[1])

    lessons_to_pay = data.get("lessons_to_pay", [])

    if lessons[lesson_id] in lessons_to_pay:
        lessons[lesson_id].remove(lessons[lesson_id])
    else:
        lessons_to_pay.append(lessons[lesson_id])

    await state.update_data(lessons_to_pay=lessons_to_pay)


    await callback_query.message.edit_reply_markup(reply_markup=create_keyboard_for_lessons(lessons))



@router.callback_query(F.data == "confirm_payment")
async def confirm_payment(callback_query: types.CallbackQuery,
                          state: FSMContext) -> None:

    data = await state.get_data()
    lessons_to_pay = data.get("lessons_to_pay")
    couples = data.get("couples_info")

    await mark_lessons_as_paid(lessons_to_pay)

    await callback_query.message.answer(payment_confirmed_message, reply_markup=edit_current_event_keyboard)

    await state.clear()






