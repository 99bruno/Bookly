from datetime import datetime

from app.database.models import (
    BookedLesson,
    Coach,
    Couple,
    Dancer,
    Lesson,
    async_session,
    Event
)
from sqlalchemy import func, outerjoin, select





async def get_all_couples_with_dancers():
    async with async_session() as session:
        result = await session.execute(
            select(
                Couple.id,
                Dancer.id,
                Dancer.full_name,
                Dancer.phone,
                Couple.id_dancer1,
                Couple.id_dancer2,
            ).join(
                Dancer,
                (Dancer.id == Couple.id_dancer1) | (Dancer.id == Couple.id_dancer2),
            )
        )
        couples_with_dancers = result.fetchall()

        couples_info = {}
        for (
            couple_id,
            dancer_id,
            dancer_name,
            dancer_phone,
            id_dancer1,
            id_dancer2,
        ) in couples_with_dancers:
            if couple_id not in couples_info:
                couples_info[couple_id] = {
                    "couple_id": couple_id,
                    "dancer1": {"name": None, "phone": None},
                    "dancer2": {"name": None, "phone": None},
                }
            if dancer_id == id_dancer1:
                couples_info[couple_id]["dancer1"] = {
                    "name": dancer_name,
                    "phone": dancer_phone,
                }
            elif dancer_id == id_dancer2:
                couples_info[couple_id]["dancer2"] = {
                    "name": dancer_name,
                    "phone": dancer_phone,
                }

        return [
            {
                "couple_id": couple_id,
                "dancer1": info["dancer1"],
                "dancer2": info["dancer2"],
            }
            for couple_id, info in couples_info.items()
        ]


async def get_lessons_grouped_by_day():
    async with async_session() as session:
        result = await session.execute(
            select(
                func.date(Lesson.start_time).label("day"),
                func.time(Lesson.start_time).label("hour"),
                (Coach.firstname + " " + Coach.lastname).label("trainer"),
                Couple.id.label("couple_id"),
                Dancer.full_name.label("dancer_name"),
            )
            .join(BookedLesson, BookedLesson.id_lesson == Lesson.id)
            .join(Couple, BookedLesson.id_couple == Couple.id)
            .join(
                Dancer,
                (Dancer.id == Couple.id_dancer1) | (Dancer.id == Couple.id_dancer2),
            )
            .join(Coach, Coach.id == Lesson.id_coach)
            .order_by("day", "hour", "trainer")
        )
        lessons = result.fetchall()

        lessons_info = []
        for day, hour, trainer, couple_id, dancer_name in lessons:
            lessons_info.append(
                {
                    "day": day,
                    "hour": hour,
                    "trainer": trainer,
                    "couple_id": couple_id,
                    "dancer_name": dancer_name,
                }
            )

        return lessons_info
