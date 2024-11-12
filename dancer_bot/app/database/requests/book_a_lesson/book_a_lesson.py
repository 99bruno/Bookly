import datetime
from collections import defaultdict

from app.database.models import BookedLesson, Coach, Lesson, async_session
from sqlalchemy import insert, select, update

currency = ["EUR", "USD", "UAH", "GBP"]


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


async def get_available_dates_by_coach_and_date(coach_id: int, date: datetime.date):
    async with async_session() as session:
        result = await session.execute(
            select(Lesson).where(Lesson.id_coach == coach_id and Lesson.date == date)
        )
        dates = result.scalars().all()

        return [
            {
                "date_id": date.id,
                "start_time": date.start_time,
                "end_time": date.end_time,
            }
            for date in dates
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

        booked_restrictions = len(result.scalars().all())

        # Filter out coach lessons that overlap with booked lessons
        lessons_by_date = defaultdict(lambda: defaultdict(int))
        lesson_restrictions = None
        for lesson, restrictions in coach_lessons:
            if (lesson.date, lesson.start_time, lesson.end_time) not in booked_times:
                date_str = lesson.date.strftime("%Y-%m-%d")
                time_range = f"{lesson.start_time.strftime('%H:%M')} - {lesson.end_time.strftime('%H:%M')}"
                lessons_by_date[date_str][time_range] = lesson.id
                lesson_restrictions = restrictions

        for lesson, restrictions in coach_lessons:
            if (lesson.date, lesson.start_time, lesson.end_time) not in booked_times:
                date_str = lesson.date.strftime("%Y-%m-%d")
                time_range = f"{lesson.start_time.strftime('%H:%M')} - {lesson.end_time.strftime('%H:%M')}"
                lessons_by_date[date_str][time_range] = lesson.id
                lesson_restrictions = restrictions

        return dict(lessons_by_date), lesson_restrictions, booked_restrictions


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


async def get_lesson_by_id(lesson_id: int):
    async with async_session() as session:
        result = await session.execute(select(Lesson).where(Lesson.id == lesson_id))
        return result.scalar_one()
