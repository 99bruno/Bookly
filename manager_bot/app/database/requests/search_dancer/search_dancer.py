import datetime
from collections import defaultdict

from app.database.models import (
    BookedLesson,
    Change,
    Coach,
    Couple,
    Currency,
    Dancer,
    Lesson,
    Payment,
    async_session,
)
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import aliased

currency = ["EUR", "USD", "UAH", "GBP"]


async def search_dancers(search_term: str, search_type: str) -> list:
    async with async_session() as session:
        async with session.begin():
            if search_type == "phone":
                result = await session.execute(
                    select(Dancer).where(Dancer.phone == search_term)
                )
            elif search_type == "name":
                result = await session.execute(
                    select(Dancer).where(Dancer.full_name.ilike(f"%{search_term}%"))
                )
            else:
                return []

            dancers = result.scalars().all()
            dancers = [
                {
                    "id": dancer.id,
                    "fullname": dancer.full_name,
                    "phone": dancer.phone,
                    "tg_id": dancer.tg_username,
                }
                for dancer in dancers
            ]
            return dancers


async def search_couples_by_dancer(dancer_id: int) -> list:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Couple).where(
                    (Couple.id_dancer1 == dancer_id) | (Couple.id_dancer2 == dancer_id)
                )
            )
            couples = result.scalars().all()
            couples_info = []
            for couple in couples:
                dancer1_result = await session.execute(
                    select(Dancer).where(Dancer.id == couple.id_dancer1)
                )
                dancer1 = dancer1_result.scalars().first()

                dancer2_result = await session.execute(
                    select(Dancer).where(Dancer.id == couple.id_dancer2)
                )
                dancer2 = dancer2_result.scalars().first()

                if dancer1 and dancer2:
                    couples_info.append(
                        {
                            "couple_id": couple.id,
                            "name": dancer1.full_name + " & " + dancer2.full_name,
                            "dancer1_id": dancer1.id,
                            "dancer2_id": dancer2.id,
                        }
                    )
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
                lesson_result = await session.execute(
                    select(Lesson).where(Lesson.id == booked_lesson.id_lesson)
                )
                lesson = lesson_result.scalars().first()
                if lesson:
                    coach_result = await session.execute(
                        select(Coach).where(Coach.id == lesson.id_coach)
                    )
                    coach = coach_result.scalars().first()

                    if lesson and coach:
                        booked_lessons_info.append(
                            {
                                "booked_lesson_id": booked_lesson.id,
                                "paid": booked_lesson.paid,
                                "lesson": {
                                    "id": lesson.id,
                                    "date": lesson.date,
                                    "start_time": lesson.start_time.strftime("%H:%M"),
                                    "end_time": lesson.end_time.strftime("%H:%M"),
                                    "available": lesson.available,
                                    "price": lesson.price,
                                    "currency": lesson.currency,
                                    "program": "Latin"
                                    if lesson.program
                                    else "Ballroom",
                                },
                                "coach": {
                                    "id": coach.id,
                                    "full_name": coach.full_name,
                                    "price": coach.price,
                                    "currency": coach.currency,
                                    "program": "Latin" if coach.program else "Ballroom",
                                },
                            }
                        )

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


async def mark_lessons_as_unpaid(booked_lesson_ids: list[int]) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(BookedLesson)
                .where(BookedLesson.id.in_(booked_lesson_ids))
                .values(paid=False)
            )
            await session.commit()


async def payment(booked_lesson_ids: list[int], manager: str) -> None:
    async with async_session() as session:
        Dancer1 = aliased(Dancer, name="Dancer1")
        Dancer2 = aliased(Dancer, name="Dancer2")

        result = await session.execute(
            select(
                BookedLesson.id,
                BookedLesson.id_coach,
                Lesson.id,
                Lesson.start_time,
                Lesson.price,
                Lesson.currency,
                BookedLesson.id_lesson,
                BookedLesson.id_couple,
                Currency.name.label("currency_name"),
                Coach.id,
                Coach.full_name.label("coach_name"),
                Dancer1.full_name.label("dancer1_name"),
                Dancer2.full_name.label("dancer2_name"),
            )
            .join(Lesson, BookedLesson.id_lesson == Lesson.id)
            .join(Coach, BookedLesson.id_coach == Coach.id)
            .join(Couple, BookedLesson.id_couple == Couple.id)
            .join(Dancer1, Couple.id_dancer1 == Dancer1.id)
            .join(Dancer2, Couple.id_dancer2 == Dancer2.id)
            .join(Currency, Lesson.currency == Currency.id)
            .where(BookedLesson.id.in_(booked_lesson_ids))
        )

        booked_lessons = result.fetchall()

        for info in booked_lessons:
            await session.execute(
                insert(Payment).values(
                    time_of_payment=datetime.datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),
                    manager_nickname=manager,
                    couple_name=info.dancer1_name + " & " + info.dancer2_name,
                    coach_name=info.coach_name,
                    lesson_date=info.start_time,
                    price=info.price,
                    currency=info.currency_name,
                )
            )

        await session.commit()


async def get_coaches_by_program(program_type: str):
    async with async_session() as session:
        result = await session.execute(
            select(Coach).where(Coach.program == (program_type == "Latin"))
        )
        x = await session.execute(select(Coach))
        coaches = result.scalars().all()

        if not coaches:
            return False

        return [
            {
                "coach_id": coach.id,
                "coach_firstname": coach.firstname,
                "coach_lastname": coach.lastname,
                "price": coach.price,
                "coach_dates": coach.dates,
            }
            for coach in coaches
        ]


async def get_lessons_by_coach(coach_id: int, couple_id: int):
    async with async_session() as session:
        # Get all available lessons for the coach
        result = await session.execute(
            select(Lesson, Coach.lesson_restrictions)
            .join(Coach, Lesson.id_coach == Coach.id)
            .where(Lesson.id_coach == coach_id, Lesson.available == True)
            .order_by(Lesson.date)
        )
        coach_lessons = result.fetchall()

        # Get all booked lessons for the dancer
        result = await session.execute(
            select(Lesson)
            .join(BookedLesson, Lesson.id == BookedLesson.id_lesson)
            .where(BookedLesson.id_couple == int(couple_id))
        )

        booked_lessons = result.scalars().all()

        # Create a set of booked time ranges
        booked_times = set(
            (lesson.date, lesson.start_time, lesson.end_time)
            for lesson in booked_lessons
        )

        result = await session.execute(
            select(Lesson)
            .join(BookedLesson, Lesson.id == BookedLesson.id_lesson)
            .where(
                BookedLesson.id_couple == int(couple_id), Lesson.id_coach == coach_id
            )
        )

        # Filter out coach lessons that overlap with booked lessons
        lessons_by_date = defaultdict(lambda: defaultdict(int))
        lesson_restrictions = None
        for lesson, restrictions in coach_lessons:
            if (lesson.date, lesson.start_time, lesson.end_time) not in booked_times:
                date_str = lesson.date.strftime("%Y-%m-%d")
                time_range = f"{lesson.start_time.strftime('%H:%M')} - {lesson.end_time.strftime('%H:%M')}"
                lessons_by_date[date_str][time_range] = lesson.id

        for lesson, restrictions in coach_lessons:
            if (lesson.date, lesson.start_time, lesson.end_time) not in booked_times:
                date_str = lesson.date.strftime("%Y-%m-%d")
                time_range = f"{lesson.start_time.strftime('%H:%M')} - {lesson.end_time.strftime('%H:%M')}"
                lessons_by_date[date_str][time_range] = lesson.id

        return dict(lessons_by_date)


async def get_lessons_info(lesson_ids: list):
    async with async_session() as session:
        result = await session.execute(
            select(Lesson, Coach)
            .join(Coach, Lesson.id_coach == Coach.id)
            .where(Lesson.id.in_(lesson_ids))
        )
        lessons = result.fetchall()

        if not lessons:
            return {}

        coach_full_name = f"{lessons[0].Coach.firstname} {lessons[0].Coach.lastname}"
        dates = [
            f"{lesson.Lesson.date.strftime('%Y-%m-%d')} {lesson.Lesson.start_time.strftime('%H:%M')} - {lesson.Lesson.end_time.strftime('%H:%M')}"
            for lesson in lessons
        ]
        dates.sort()  # Sort the dates
        total_sum = sum(lesson.Lesson.price for lesson in lessons)

        return {
            "coach_full_name": coach_full_name,
            "dates": dates,
            "total_sum": str(total_sum) + " " + currency[lessons[0].Coach.currency - 1],
        }


async def book_lessons(lesson_ids: list, couple_id: int, coach_id: int) -> list:
    async with async_session() as session:
        # Get the lessons to be booked
        result = await session.execute(select(Lesson).where(Lesson.id.in_(lesson_ids)))
        lessons = result.scalars().all()

        # Check for unavailable lessons
        unavailable_lessons = [
            (
                f"{lesson.date} "
                f"{lesson.start_time.strftime('%H:%M')} - {lesson.end_time.strftime('%H:%M')}"
            )
            for lesson in lessons
            if not lesson.available
        ]
        available_lessons = [lesson.id for lesson in lessons if lesson.available]

        await session.execute(
            update(Lesson)
            .where(Lesson.id.in_(available_lessons))
            .values(available=False)
        )

        # Insert new records into the booked_lessons table
        for lesson_id in available_lessons:
            await session.execute(
                insert(BookedLesson).values(
                    id_lesson=lesson_id,
                    id_couple=couple_id,
                    id_coach=coach_id,
                    paid=False,
                )
            )

        await session.commit()
        return unavailable_lessons


async def cancel_booked_lesson(
    booked_lesson_id: int, data: dict, username: str
) -> None:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(BookedLesson.id_lesson).where(
                    BookedLesson.id == booked_lesson_id
                )
            )
            lesson_id = result.scalar()

            await session.execute(
                delete(BookedLesson).where(BookedLesson.id == booked_lesson_id)
            )

            await session.execute(
                update(Lesson).where(Lesson.id == lesson_id).values(available=True)
            )

            await session.execute(
                insert(Change).values(
                    time_of_change=datetime.datetime.now().strftime("%D-%m-%Y %H:%M"),
                    dancer_username="TBA" if username is None else username,
                    couple_name=data["couples_info"][data["current_couple_id"]]["name"],
                    coach_name=data["lessons"][data["current_couple_id"]]["coach"][
                        "full_name"
                    ],
                    lesson_date=data["lesson_date"],
                    lesson_id=lesson_id,
                    reason=data["reason"],
                )
            )

            await session.commit()


async def get_coach_name(booked_lesson_id: int) -> str:
    async with async_session() as session:
        # Check if the new lesson is available
        result = await session.execute(
            select(Coach.full_name)
            .join(BookedLesson, BookedLesson.id_coach == Coach.id)
            .where(BookedLesson.id == booked_lesson_id)
        )

        return result.scalar()


async def get_available_lessons_by_lesson_id(lesson_id: int) -> list:
    async with async_session() as session:
        # Отримати lesson за lesson_id
        lesson_idx_result = await session.execute(
            select(BookedLesson).where(BookedLesson.id == lesson_id)
        )
        lesson_idx = lesson_idx_result.scalar()

        result = await session.execute(
            select(Lesson).where(Lesson.id == lesson_idx.id_lesson)
        )
        lesson = result.scalars().first()

        # Отримати coach для цього уроку
        coach_info = await session.execute(
            select(Coach).where(Coach.id == lesson.id_coach)
        )

        coach = coach_info.scalars().first()

        if not lesson:
            return []

        # Отримати всі доступні уроки для цього тренера на ту ж дату
        result = await session.execute(
            select(Lesson)
            .where(
                Lesson.id_coach == lesson.id_coach,
                Lesson.date == lesson.date,
                Lesson.available == True,
            )
            .order_by(Lesson.start_time)
        )

        available_lessons = result.scalars().all()

        # Перевірити, чи не накладаються ці уроки по часу на інші уроки цього танцівника
        booked_lessons_result = await session.execute(
            select(Lesson)
            .join(BookedLesson, BookedLesson.id_lesson == Lesson.id)
            .where(BookedLesson.id_couple == lesson_idx.id_couple)
        )
        booked_lessons = booked_lessons_result.scalars().all()

        def is_time_conflict(lesson1, lesson2):
            return not (
                lesson1.end_time <= lesson2.start_time
                or lesson1.start_time >= lesson2.end_time
            )

        available_lessons = [
            {
                "id": available_lesson.id,
                "start_time": available_lesson.start_time,
                "end_time": available_lesson.end_time,
                "coach": coach.full_name,
            }
            for available_lesson in available_lessons
            if all(
                not is_time_conflict(available_lesson, booked_lesson)
                for booked_lesson in booked_lessons
            )
        ]

        return available_lessons


async def reschedule_lesson(booked_lesson_id: int, new_lesson_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(select(Lesson).where(Lesson.id == new_lesson_id))
        new_lesson = result.scalars().first()

        if not new_lesson or not new_lesson.available:
            return False

        result = await session.execute(
            select(BookedLesson.id_lesson).where(BookedLesson.id == booked_lesson_id)
        )
        current_lesson_id = result.scalar()

        await session.execute(
            update(BookedLesson)
            .where(BookedLesson.id == booked_lesson_id)
            .values(id_lesson=new_lesson_id)
        )

        await session.execute(
            update(Lesson).where(Lesson.id == current_lesson_id).values(available=True)
        )

        await session.execute(
            update(Lesson).where(Lesson.id == new_lesson_id).values(available=False)
        )

        await session.commit()

        return True
