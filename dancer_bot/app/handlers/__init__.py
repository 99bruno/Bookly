from aiogram import Router

from .start.start import router as start_router
from .book_a_lesson.book_a_lesson import router as book_a_lesson_router
from .check_schedules.check_schedules import router as check_schedules_router
from .check_schedules.register_user import router as register_user_router_schedule
from .check_camp_info.check_camp_info import router as check_camp_info_router
from .get_help_from_manager.get_help_from_manager import router as get_help_from_manage_router
from .book_a_lesson.register_user import router as register_user_router


def register_all_handlers():
    router = Router()

    router.include_router(start_router)
    router.include_router(book_a_lesson_router)
    router.include_router(register_user_router)
    router.include_router(register_user_router_schedule)
    router.include_router(check_schedules_router)
    router.include_router(check_camp_info_router)
    router.include_router(get_help_from_manage_router)

    return router
