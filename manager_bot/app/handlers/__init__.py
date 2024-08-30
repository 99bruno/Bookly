from aiogram import Router

from .start.start import router as start_router
from .coaches.coaches import router as coaches_router
from .coaches.add_coach import router as add_coach_router
from .create_event.create_event import router as create_event_router
from .edit_current_event.edit_current_event import router as edit_current_event_router
from .dancers.dancers import router as dancers_router
from .camp_info.edit_camp_info import router as edit_camp_info_router


def register_all_handlers():
    router = Router()

    router.include_router(start_router)
    router.include_router(coaches_router)
    router.include_router(add_coach_router)
    router.include_router(create_event_router)
    router.include_router(edit_current_event_router)
    router.include_router(dancers_router)
    router.include_router(edit_camp_info_router)

    return router
