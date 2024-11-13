import ast
from datetime import date, datetime, time, timedelta
from typing import Any, Dict, List

from app.database.models import Coach, Lesson, ScheduleEvent, async_session
from sqlalchemy import select, update


async def get_days_of_camp(idx: int = 1) -> list[Any]:
    async with async_session() as session:
        result = await session.scalar(
            select(ScheduleEvent).where(ScheduleEvent.id == idx)
        )

        return ast.literal_eval(ast.literal_eval(result.dates))


async def get_coach_by_a_date(date_of_camp: str) -> dict[str:int]:
    async with async_session() as session:
        result = await session.execute(
            select(Lesson, Coach.full_name, Coach.id)
            .distinct()
            .join(Coach, Lesson.id_coach == Coach.id)
            .where(Lesson.date == datetime.strptime(date_of_camp, "%d.%m.%Y").date())
        )

        return {f"{res.full_name}": res.id for res in result}


async def get_lessons_by_a_coach_and_date_and_not_booked(
    coach_id: int, date_of_camp: str
) -> dict[str, Any]:
    async with async_session() as session:
        result = await session.execute(
            select(Lesson.id, Lesson.start_time).where(
                Lesson.id_coach == coach_id,
                Lesson.date == datetime.strptime(date_of_camp, "%d.%m.%Y").date(),
                Lesson.available == True,
            )
        )

        return {f"{res.start_time.strftime("%H:%M")}": res.id for res in result}


async def block_lesson_by_id(lesson_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Lesson).where(Lesson.id == lesson_id).values(available=False)
            )
