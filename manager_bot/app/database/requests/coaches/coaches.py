import datetime

from app.database.models import (
    BookedLesson,
    Coach,
    Couple,
    Dancer,
    Lesson,
    async_session,
)
from sqlalchemy import select


async def get_all_coaches() -> list:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Coach))
            coaches = result.scalars().all()

            coaches_dict = [
                {
                    "id": coach.id,
                    "coach": coach.full_name,
                    "program": coach.program,
                    "price": coach.price,
                    "currency": coach.currency,
                    "dates": coach.dates,
                    "name": coach.firstname,
                    "surname": coach.lastname,
                    "lesson_restrictions": coach.lesson_restrictions,
                }
                for coach in coaches
            ]

            return coaches_dict


async def update_coach_info(coach_id: int, column: str, new_value) -> bool:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Coach).where(Coach.id == coach_id))
            coach = result.scalars().first()

            if coach:
                if column == "firstname":
                    setattr(coach, column, new_value)
                    setattr(coach, "full_name", new_value + " " + coach.lastname)

                elif column == "lastname":
                    setattr(coach, column, new_value)
                    setattr(coach, "full_name", coach.firstname + " " + new_value)

                setattr(coach, column, new_value)
                await session.commit()
                return True
            else:
                return False


async def view_coach_schedule(coach_id: int, date: datetime.date) -> list:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Lesson).where(Lesson.id_coach == coach_id, Lesson.date == date)
            )
            lessons = result.scalars().all()

            lessons_info = []
            for lesson in lessons:
                lesson_info = {
                    "id": lesson.id,
                    "id_coach": lesson.id_coach,
                    "available": lesson.available,
                    "date": lesson.date,
                    "time": lesson.start_time.strftime("%H:%M")
                    + "-"
                    + lesson.end_time.strftime("%H:%M"),
                }

                if not lesson.available:
                    booked_lesson_result = await session.execute(
                        select(BookedLesson).where(BookedLesson.id_lesson == lesson.id)
                    )
                    booked_lesson = booked_lesson_result.scalars().first()

                    if booked_lesson:
                        couple_result = await session.execute(
                            select(Couple).where(Couple.id == booked_lesson.id_couple)
                        )
                        couple = couple_result.scalars().first()

                        if couple:
                            dancer1_result = await session.execute(
                                select(Dancer).where(Dancer.id == couple.id_dancer1)
                            )
                            dancer1 = dancer1_result.scalars().first()

                            dancer2_result = await session.execute(
                                select(Dancer).where(Dancer.id == couple.id_dancer2)
                            )
                            dancer2 = dancer2_result.scalars().first()

                            if dancer1 and dancer2:
                                lesson_info["couple"] = {
                                    "couples_name": dancer1.full_name
                                    + " - "
                                    + dancer2.full_name,
                                    "paid_status": booked_lesson.paid,
                                    "dancer1": {
                                        "name": dancer1.name,
                                        "surname": dancer1.surname,
                                        "full_name": dancer1.full_name,
                                    },
                                    "dancer2": {
                                        "name": dancer2.name,
                                        "surname": dancer2.surname,
                                        "full_name": dancer2.full_name,
                                    },
                                }

                lessons_info.append(lesson_info)

            return lessons_info
