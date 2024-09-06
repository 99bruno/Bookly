from datetime import datetime, date, time, timedelta
import ast
from typing import List, Any

from sqlalchemy import select
from app.database.models import Coach, Lesson, ScheduleEvent, async_session

currency = ["USD", "EUR", "UAH", "GBP",]


async def get_days_of_the_camp(idx: int=1) -> list[Any]:
    async with async_session() as session:
            result = await session.scalar(select(ScheduleEvent).where(ScheduleEvent.id == idx))

            return [ast.literal_eval(ast.literal_eval(result.dates)),
                    ast.literal_eval(result.full_schedule)]


async def add_coach_to_db(data: dict, lessons: list) -> None:
    async with async_session() as session:
        async with session.begin():
            coach = Coach(firstname=data["name"],
                          lastname=data["surname"],
                          full_name=data["name"] + " " + data["surname"],
                          id_event=1,
                          program=data["program"],
                          dates=str(data["dates"]),
                          price=int(data["price"]),
                          currency=currency.index(data["currency"])+1,
                          lesson_restrictions=4
                          )
            session.add(coach)

            await session.flush()

            for lesson_date in data["dates"]:
                lesson_date = datetime.strptime(lesson_date, '%d.%m.%Y').date()
                for lesson in lessons:
                    start_time = lesson.split("-")[0].split(":")
                    end_time = lesson.split("-")[-1].split(":")
                    new_lesson = Lesson(
                        id_coach=coach.id,
                        available=True,
                        start_time=datetime.combine(lesson_date, time(int(start_time[0]), int(start_time[-1]))),
                        end_time=datetime.combine(lesson_date, time(int(end_time[0]), int(end_time[-1]))),
                        date=lesson_date,
                        price=int(data["price"]),
                        currency=currency.index(data["currency"])+1,
                        program=data["program"]
                    )
                    session.add(new_lesson)

            await session.commit()