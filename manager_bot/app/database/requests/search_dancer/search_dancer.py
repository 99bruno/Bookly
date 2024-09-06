import datetime

from sqlalchemy import select, update, insert
from sqlalchemy.orm import aliased
from app.database.models import async_session, BookedLesson, Lesson, Coach, Couple, Dancer, Currency, Payment


async def search_dancers(search_term: str, search_type: str) -> list:
    async with async_session() as session:
        async with session.begin():
            if search_type == "phone":
                result = await session.execute(select(Dancer).where(Dancer.phone == search_term))
            elif search_type == "name":
                result = await session.execute(select(Dancer).where(Dancer.full_name.ilike(f"%{search_term}%")))
            else:
                return []

            dancers = result.scalars().all()
            dancers = [{"id": dancer.id,
                        "fullname": dancer.full_name,
                        "phone": dancer.phone,
                        "tg_id": dancer.tg_username,
                        }
                       for dancer in dancers]
            return dancers


async def search_couples_by_dancer(dancer_id: int) -> list:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Couple).where((Couple.id_dancer1 == dancer_id) | (Couple.id_dancer2 == dancer_id))
            )
            couples = result.scalars().all()
            couples_info = []
            for couple in couples:
                dancer1_result = await session.execute(select(Dancer).where(Dancer.id == couple.id_dancer1))
                dancer1 = dancer1_result.scalars().first()

                dancer2_result = await session.execute(select(Dancer).where(Dancer.id == couple.id_dancer2))
                dancer2 = dancer2_result.scalars().first()

                if dancer1 and dancer2:
                    couples_info.append({
                        "couple_id": couple.id,
                        "name": dancer1.full_name + " & " + dancer2.full_name,
                        "dancer1_id": dancer1.id,
                        "dancer2_id": dancer2.id})
            return couples_info


async def get_booked_lessons_for_couple(couple_id: int) -> list:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(BookedLesson).where(BookedLesson.id_couple == couple_id)
            )
            booked_lessons = result.scalars().all()
            booked_lessons_info = []
            for booked_lesson in booked_lessons:
                lesson_result = await session.execute(select(Lesson).where(Lesson.id == booked_lesson.id_lesson))
                lesson = lesson_result.scalars().first()
                if lesson:

                    coach_result = await session.execute(select(Coach).where(Coach.id == lesson.id_coach))
                    coach = coach_result.scalars().first()

                    if lesson and coach:
                        booked_lessons_info.append({
                            "booked_lesson_id": booked_lesson.id,
                            "paid": booked_lesson.paid,
                            "lesson": {
                                "id": lesson.id,
                                "date": lesson.date,
                                "start_time": lesson.start_time.strftime('%H:%M'),
                                "end_time": lesson.end_time.strftime('%H:%M'),
                                "available": lesson.available,
                                "price": lesson.price,
                                "currency": lesson.currency,
                                "program": "Latin" if lesson.program else "Ballroom"
                            },
                            "coach": {
                                "id": coach.id,
                                "full_name": coach.full_name,
                                "price": coach.price,
                                "currency": coach.currency,
                                "program": "Latin" if coach.program else "Ballroom"
                            }
                        })

            return booked_lessons_info


async def mark_lessons_as_paid(booked_lesson_ids: list[int]) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(BookedLesson)
                .where(BookedLesson.id.in_(booked_lesson_ids))
                .values(paid=True)
            )

            await session.commit()


async def payment(booked_lesson_ids: list[int], manager: str) -> None:
    async with async_session() as session:
        Dancer1 = aliased(Dancer, name='Dancer1')
        Dancer2 = aliased(Dancer, name='Dancer2')

        result = await session.execute(
            select(BookedLesson.id,
                   BookedLesson.id_coach,
                   Lesson.id,
                   Lesson.start_time,
                   Lesson.price,
                   Lesson.currency,
                   BookedLesson.id_lesson,
                   BookedLesson.id_couple,
                   Currency.name.label("currency_name"),
                   Coach.id,
                   Coach.full_name.label('coach_name'),
                   Dancer1.full_name.label('dancer1_name'),
                   Dancer2.full_name.label('dancer2_name'))
            .join(Lesson, BookedLesson.id_lesson == Lesson.id)
            .join(Coach, BookedLesson.id_coach == Coach.id)
            .join(Couple, BookedLesson.id_couple == Couple.id)
            .join(Dancer1, Couple.id_dancer1 == Dancer1.id)
            .join(Dancer2, Couple.id_dancer2 == Dancer2.id)
            .join(Currency, Lesson.currency == Currency.id)
            .where(BookedLesson.id.in_(booked_lesson_ids)))

        booked_lessons = result.fetchall()

        for info in booked_lessons:
            await session.execute(
                insert(Payment).values(
                    time_of_payment=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                    manager_nickname=manager,
                    couple_name=info.dancer1_name + " & " + info.dancer2_name,
                    coach_name=info.coach_name,
                    lesson_date=info.start_time,
                    price=info.price,
                    currency=info.currency_name
                )
            )

        await session.commit()