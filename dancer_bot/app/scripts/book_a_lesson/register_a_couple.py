from aiogram import types, html, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


from app.templates.book_a_lesson.book_a_lesson import *

from app.keyboards.start.start import back_to_main_menu_keyboard
from app.keyboards.book_a_lesson.book_a_lesson import *

from app.database.requests.book_a_lesson.check_dancer import check_user_registered, add_user, check_couple_registered

from app.scripts.auxiliary_functions.format_strings import format_string
from app.scripts.book_a_lesson.book_a_lesson import concatenate_couples, format_couple

from app.states.book_a_lesson.register_dancer import UserRegistration, Couple


