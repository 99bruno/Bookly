from aiogram.fsm.state import State, StatesGroup


class NewEvent(StatesGroup):
    name = State()  # Name of the event
    description = State()  # Description of the event
    type_of_schedule = State()  # Type of schedule: for every day or for all dates
    dates = State()  # List of dates
    add_breaks = State()  # Add breaks

    single_template = State()  # Single template for all dates
    multiple_templates = State()  # Template for each day

    start_time = State()  # List of start times or start time for all dates
    end_time = State()  # List of end times or end time for all dates
    lesson_duration = State()  # Lesson duration in minutes
    breaks = State()  # List of breaks

    final_schedule = State()  # List of schedules for each day
