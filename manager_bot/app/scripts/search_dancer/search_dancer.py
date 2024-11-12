from collections import defaultdict
from datetime import date, datetime
from typing import Any, Dict, List

currency = ["EUR", "USD", "UAH", "GBP"]


async def dancers_list_message_unpack(dancers: list, template: str) -> str:
    return template.format(
        "\n".join(
            [
                f"{idx+1}. {dancer['fullname']} - +{dancer['phone']}"
                for idx, dancer in enumerate(dancers)
            ]
        )
    )


async def dancer_info_message_unpack(dancer: dict, template: str, couples: list) -> str:
    return template.format(
        dancer["fullname"],
        dancer["phone"],
        dancer["tg_id"],
        "\n".join([f"{idx+1}. {couple['name']}" for idx, couple in enumerate(couples)]),
    )


async def couple_info_message_unpack(couple: dict, template: str, schedule) -> str:
    return template.format(couple["name"], await format_booked_lessons(schedule))


async def format_booked_lessons(booked_lessons: list) -> str:
    lessons_by_date = defaultdict(list)
    total_unpaid_price = {"USD": 0, "EUR": 0, "UAH": 0, "GBP": 0}

    for lesson in booked_lessons:
        lesson_date = lesson["lesson"]["date"]
        lessons_by_date[lesson_date].append(lesson)
        if not lesson["paid"]:
            total_unpaid_price[currency[lesson["lesson"]["currency"] - 1]] += lesson[
                "lesson"
            ]["price"]

    formatted_output = []
    for lesson_date, lessons in sorted(lessons_by_date.items()):
        formatted_output.append(f"\n{lesson_date.strftime('%d-%m-%Y')}\n")
        for lesson in sorted(lessons, key=lambda x: x["lesson"]["start_time"]):
            start_time = lesson["lesson"]["start_time"]
            end_time = lesson["lesson"]["end_time"]
            paid_status = "✅" if lesson["paid"] else "❌"
            price = lesson["lesson"]["price"]
            currency_ = currency[lesson["lesson"]["currency"] - 1]
            program = lesson["lesson"]["program"]
            coach_name = lesson["coach"]["full_name"]
            formatted_output.append(
                f"‣ {start_time}-{end_time} | {coach_name} | {price} {currency_} | {paid_status}"
            )

    formatted_output.append(
        f"\nTotal unpaid price: "
        f"{'' if not total_unpaid_price['USD'] else str(total_unpaid_price['USD'])+'USD'} "
        f"{'' if not total_unpaid_price['EUR'] else str(total_unpaid_price['EUR'])+'EUR'} "
        f"{'' if not total_unpaid_price['UAH'] else str(total_unpaid_price['UAH'])+'UAH'} "
        f"{'' if not total_unpaid_price['GBP'] else str(total_unpaid_price['GBP'])+'GBP'} "
    )
    return "\n".join(formatted_output)


async def sort_lessons(schedules: list) -> dict[str, Any]:
    lessons_by_date = defaultdict(list)

    formated_output = dict()
    for lesson in schedules:
        lesson_date = lesson["lesson"]["date"]
        lessons_by_date[lesson_date].append(lesson)

    for lesson_date, lessons in sorted(lessons_by_date.items()):
        for lesson in sorted(lessons, key=lambda x: x["lesson"]["start_time"]):
            formated_output[
                f'{lesson_date.strftime("%d-%m")} {lesson["lesson"]["start_time"]} {lesson["coach"]["full_name"]}'
            ] = int(lesson["booked_lesson_id"])

    return formated_output


async def sort_lessons_test(schedules: list) -> dict[str, Any]:
    lessons_by_date = defaultdict(list)

    formated_output = dict()
    for lesson in schedules:
        lesson_date = lesson["date"]
        lessons_by_date[lesson_date].append(lesson)

    for lesson_date, lessons in sorted(lessons_by_date.items()):
        for lesson in sorted(lessons, key=lambda x: x["start_time"]):
            formated_output[
                (
                    f'{lesson_date.strftime("%d.%m")}  '
                    f'{lesson["start_time"].strftime("%H:%M")} - {lesson["coach"]}'
                )
            ] = int(lesson["id"])

    return formated_output


async def sort_lessons_test_2(schedules: List[Dict[str, Any]]) -> Dict[str, Any]:
    lessons_by_date = defaultdict(list)
    formated_output = dict()

    # Group lessons by date
    for lesson in schedules:
        lesson_date = lesson["lesson"]["date"]
        lessons_by_date[lesson_date].append(lesson)

    # Sort and format lessons
    for lesson_date, lessons in sorted(lessons_by_date.items()):
        for lesson in sorted(lessons, key=lambda x: x["lesson"]["start_time"]):
            formated_output[
                (
                    f'{lesson_date.strftime("%d.%m")}  '
                    f'{lesson["lesson"]["start_time"]} - {lesson["coach"]["full_name"]}'
                )
            ] = int(lesson["booked_lesson_id"])

    return formated_output


def format_lesson_info(lesson_info: dict, template: str) -> str:
    dates = "\n".join(lesson_info["dates"])
    total_sum = lesson_info["total_sum"]

    return template.format(dates, total_sum)


def format_string(template, info_list):
    return template.format(*info_list)
