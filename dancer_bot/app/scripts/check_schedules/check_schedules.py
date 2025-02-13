from collections import defaultdict
from typing import Any, Dict

currency = ["EUR", "USD", "UAH", "GBP"]


def format_schedules(schedule: list[dict]) -> str:
    import datetime

    return "\n\n".join(
        [
            f"•Заняття {idx+1}\nДата: {info['date'].strftime('%d-%m-%Y')} {info['time']}"
            f"\nТренер: {info['coach']}\nЦіна: {info['price']}"
            for idx, info in enumerate(schedule)
        ]
    )


def format_schedule(schedule: dict) -> str:
    import datetime

    return (
        f"Дата: {schedule['date'].strftime('%d-%m-%Y')} "
        f"{schedule['time']}\nТренер: {schedule['coach']}\nЦіна: {schedule['price']}"
    )


async def format_reschedule_lessons(lessons: list) -> str:
    return "\n".join([f"• {lesson["start_time"]}" for lesson in lessons])


async def format_booked_lessons(booked_lessons: list) -> str:
    lessons_by_date = defaultdict(list)
    total_unpaid_price = {"EUR": 0, "USD": 0, "UAH": 0, "GBP": 0}

    for lesson in booked_lessons:
        lesson_date = lesson["date"]
        lessons_by_date[lesson_date].append(lesson)
        if not lesson["paid"]:
            total_unpaid_price[currency[lesson["currency"] - 1]] += lesson["price"]

    formatted_output = []
    for lesson_date, lessons in sorted(lessons_by_date.items()):
        formatted_output.append(f"<b>\n{lesson_date.strftime('%d-%m-%Y')}\n</b>")
        for lesson in sorted(lessons, key=lambda x: x["start_time"]):
            time = lesson["time"]
            paid_status = "✅" if lesson["paid"] else "❌"
            price = lesson["price"]
            currency_ = currency[lesson["currency"] - 1]
            coach_name = lesson["coach"]
            formatted_output.append(
                f"‣ {time} | {coach_name} | {price} {currency_} | {paid_status}"
            )

    formatted_output.append(
        f"\n<b>Сума до сплати: </b>"
        f"{'' if not total_unpaid_price['USD'] else str(total_unpaid_price['USD'])+' USD'} "
        f"{'' if not total_unpaid_price['EUR'] else str(total_unpaid_price['EUR'])+' EUR'} "
        f"{'' if not total_unpaid_price['UAH'] else str(total_unpaid_price['UAH'])+' UAH'} "
        f"{'' if not total_unpaid_price['GBP'] else str(total_unpaid_price['GBP'])+' GBP'} "
        f" <b>+ оплата за збори</b>"
    )
    return "\n".join(formatted_output)


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


async def sort_lessons(schedules: list) -> dict[str, Any]:
    lessons_by_date = defaultdict(list)

    formated_output = dict()
    for lesson in schedules:
        lesson_date = lesson["date"]
        lessons_by_date[lesson_date].append(lesson)

    for lesson_date, lessons in sorted(lessons_by_date.items()):
        for lesson in sorted(lessons, key=lambda x: x["start_time"]):
            formated_output[f'{lesson_date.strftime("%d-%m")} {lesson["time"]}'] = int(
                lesson["id"]
            )

    return formated_output
