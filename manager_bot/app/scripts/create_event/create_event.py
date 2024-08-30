import re
from datetime import datetime, timedelta


def validate_date_range(date_range: str) -> (bool, [str, list]):
    # Regular expression to match the date format
    date_pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}$')

    if not date_pattern.match(date_range):
        return False, "Invalid date format 🥲\n\n"

    try:
        start_date_str, end_date_str = date_range.split('-')
        start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
        end_date = datetime.strptime(end_date_str, '%d.%m.%Y')

        # Ensure start date is before end date
        if start_date > end_date:
            return False, "Start date cannot be after end date"

        # Ensure start date is not in the past
        if start_date < datetime.now():
            return False, "Start date cannot be in the past"

        date_list = []
        current_date = start_date
        while current_date <= end_date:
            date_list.append(current_date.strftime('%d.%m.%Y'))
            current_date += timedelta(days=1)

        return True, date_list

    except ValueError:
        return False, "Error parsing dates"


def validate_time(time_str: str) -> (bool, str):
    # Regular expression to match the time format
    time_pattern = re.compile(r'^\d{2}:\d{2}$')

    if not time_pattern.match(time_str):
        return False, ("<b>Invalid Time Format  😕</b>"
                       "Please use the format <b>HH:MM</b>. For example: <b>12:00</b>."
                       "If you want 8:00, please type <b>08:00</b>.")

    try:
        # Ensure time is valid
        datetime.strptime(time_str, '%H:%M')
        return True, time_str

    except ValueError:
        return False, "Error parsing time"


def validate_breaks(breaks: str) -> (bool, [str, list]):
    # Regular expression to match the break format
    break_pattern = re.compile(r'^\d{2}:\d{2}-\d{2}:\d{2}$')

    breaks_list = breaks.split('\n')
    for break_time in breaks_list:
        if not break_pattern.match(break_time):
            return False, "Invalid break format"

        start_time_str, end_time_str = break_time.split('-')
        start_time = datetime.strptime(start_time_str, '%H:%M')
        end_time = datetime.strptime(end_time_str, '%H:%M')

        # Ensure start time is before end time
        if start_time >= end_time:
            return False, "Start time cannot be after end time"

    return True, breaks_list


def validate_all_parameters(data: dict) -> bool:
    required_parameters = ['start_time', 'end_time', 'breaks', 'lesson_duration']
    for param in required_parameters:
        if data.get(param) is None:
            return False
    return True


from datetime import datetime, timedelta


from datetime import datetime, timedelta

def generate_schedule(start_time: str, end_time: str, lesson_duration: int, breaks: list) -> (bool, list):
    start_time_dt = datetime.strptime(start_time, '%H:%M')
    end_time_dt = datetime.strptime(end_time, '%H:%M')
    lesson_duration_td = timedelta(minutes=lesson_duration)

    schedule = []
    current_time = start_time_dt

    breaks_dt = []
    for break_time in breaks:
        break_start_str, break_end_str = break_time.split('-')
        break_start = datetime.strptime(break_start_str, '%H:%M')
        break_end = datetime.strptime(break_end_str, '%H:%M')
        breaks_dt.append((break_start, break_end))

    while current_time + lesson_duration_td <= end_time_dt:
        lesson_start = current_time
        lesson_end = current_time + lesson_duration_td

        # Check for overlap with breaks
        overlap = False
        for break_start, break_end in breaks_dt:
            if (lesson_start < break_end and lesson_end > break_start):
                overlap = True
                current_time = break_end  # Move current time to the end of the break
                break

        if not overlap:
            schedule.append(f"{lesson_start.strftime('%H:%M')}-{lesson_end.strftime('%H:%M')}")
            current_time += lesson_duration_td

    if not schedule:
        return False, "Unable to generate schedule with the given parameters."

    return True, schedule


def single_template_message_unpack(
                                   template: str,
                                   data: dict,
                                   ) -> str:

    return template.format(", ".join(data["dates"]),
                           "" if data["start_time"] is None else data["start_time"],
                           "" if data["end_time"]  is None else data["end_time"],
                           "" if data["lesson_duration"]  is None else data["lesson_duration"],
                           single_event_breaks_unpack(data["breaks"]),)


def single_event_created_message_unpack(template: str, data: dict) -> str:

        return template.format(data["name"],
                               ", ".join(data["dates"]),
                               data["description"],
                               "\n".join([f"<b>•Lesson</b> {idx+1}: {day_schedule}" for idx, day_schedule in enumerate(data["final_schedule"])]))


def single_event_breaks_unpack(breaks: (list, None)) -> str:

    return "" if breaks is None else "\n\t\t\t"+"\t\t\t".join([f"•Break {idx+1}: {break_time}\n" for idx, break_time in enumerate(breaks)])


def single_event_breaks_message_unpack(breaks: (list, None),
                                       template: str
                                       ) -> str:

    return template.format(single_event_breaks_unpack(breaks))


def created_schedule_message_unpack(
                                   template: str,
                                   schedule: list,
                                   ) -> str:

    return template.format("\n".join([f"•Lesson {idx+1}: {day_schedule}" for idx, day_schedule in enumerate(schedule)]))