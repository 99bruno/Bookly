from aiogram import Router

from .start.start import router as start_router
from .view_and_edit_coaches.view_and_edit_coaches import router as view_and_edit_coaches_router
from .search_dancer.search_dancer import router as search_dancer_router
from .view_full_schedule.view_full_schedule import router as view_full_schedule_router
from .camp_settings.camp_settings_main import router as camp_settings_router
from .camp_settings.coaches_settings.coaches_settings import router as coaches_settings_router
from .camp_settings.coaches_settings.add_new_coach import router as add_coach_router

from .camp_settings.camp_settings.edit_camp_info import router as edit_camp_info_router
from .camp_settings.camp_settings.camp_settings import router as camp_settings_edit_router


from .settings.settings import router as settings_router
from .settings.managers import router as managers_router
from .settings.create_event import router as create_event_router

"""from .start.start import router as start_router
from manager_bot.app.handlers.test.coaches_settings.coaches_settings import router as coaches_settings_router
from manager_bot.app.handlers.test.coaches_settings.add_new_coach import router as add_coach_router
from manager_bot.app.handlers.test.coaches_settings.view_and_edit import router as view_and_edit_router
from manager_bot.app.handlers.test.settings.settings import router as settings_router
from manager_bot.app.handlers.test.settings.managers import router as managers_router
from manager_bot.app.handlers.test.camp_settings.camp_settings import router as camp_settings_router"""


# from .coaches.coaches import router as coaches_router
# from .coaches.add_coach import router as add_coach_router
# from .create_event.create_event import router as create_event_router
# from .edit_current_event.edit_current_event import router as edit_current_event_router
# from .dancers.dancers import router as dancers_router
# from .view_full_schedule.edit_camp_info import router as edit_camp_info_router


def register_all_handlers():
    router = Router()

    router.include_router(start_router)
    router.include_router(view_and_edit_coaches_router)
    router.include_router(search_dancer_router)
    router.include_router(view_full_schedule_router)
    router.include_router(camp_settings_router)
    router.include_router(coaches_settings_router)
    router.include_router(add_coach_router)
    router.include_router(edit_camp_info_router)
    router.include_router(camp_settings_edit_router)

    router.include_router(settings_router)
    router.include_router(managers_router)
    router.include_router(create_event_router)


    """router.include_router(start_router)
    router.include_router(coaches_settings_router)
    router.include_router(add_coach_router)
    router.include_router(view_and_edit_router)

    router.include_router(settings_router)
    router.include_router(managers_router)

    router.include_router(camp_settings_router)"""

    # router.include_router(coaches_router)
    # router.include_router(add_coach_router)
    # router.include_router(create_event_router)
    # router.include_router(edit_current_event_router)
    # router.include_router(dancers_router)
    # router.include_router(edit_camp_info_router)

    return router
