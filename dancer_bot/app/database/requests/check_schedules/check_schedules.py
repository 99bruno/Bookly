from sqlalchemy import select, delete, update
from app.database.models import async_session, Lesson, BookedLesson, Coach, Couple


async def check_couple_exists(dancer1_id: int, dancer2_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(Couple).where(
                (Couple.id_dancer1 == dancer1_id) & (Couple.id_dancer2 == dancer2_id) |
                (Couple.id_dancer1 == dancer2_id) & (Couple.id_dancer2 == dancer1_id)
            )
        )
        couple = result.scalars().first()

        return couple is not None


async def get_booked_lessons_by_couple(couple_id: int) -> list:
    async with async_session() as session:

        result = await session.execute(
            select(Lesson.date, Coach.firstname, Coach.lastname, Lesson.price, Lesson.currency, BookedLesson.id,
                   Lesson.start_time, Lesson.end_time, BookedLesson.paid)
            .join(BookedLesson, BookedLesson.id_lesson == Lesson.id)
            .join(Coach, Coach.id == Lesson.id_coach)
            .where(BookedLesson.id_couple == couple_id)
        )
        booked_lessons = result.fetchall()

        lessons_info = [
            {"id": lesson.id, "date": lesson.date, "coach": lesson.firstname+" "+lesson.lastname, "price": lesson.price,
             "currency": lesson.currency, "paid": lesson.paid, "start_time": lesson.start_time,
             "time": lesson.start_time.strftime("%H:%M")+ " - "+lesson.end_time.strftime("%H:%M")}
            for lesson in booked_lessons
        ]

        return lessons_info


async def cancel_booked_lesson(booked_lesson_id: int) -> None:
    async with async_session() as session:
        async with session.begin():

            result = await session.execute(
                select(BookedLesson.id_lesson)
                .where(BookedLesson.id == booked_lesson_id)
            )
            lesson_id = result.scalar()

            await session.execute(
                delete(BookedLesson)
                .where(BookedLesson.id == booked_lesson_id)
            )

            await session.execute(
                update(Lesson)
                .where(Lesson.id == lesson_id)
                .values(available=True)
            )

            await session.commit()


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
            select(Lesson).where(
                Lesson.id_coach == lesson.id_coach,
                Lesson.date == lesson.date,
                Lesson.available == True
            ).order_by(Lesson.start_time)
        )

        available_lessons = result.scalars().all()

        # Перевірити, чи не накладаються ці уроки по часу на інші уроки цього танцівника
        booked_lessons_result = await session.execute(
            select(Lesson).join(BookedLesson, BookedLesson.id_lesson == Lesson.id)
            .where(BookedLesson.id_couple == lesson_idx.id_couple)
        )
        booked_lessons = booked_lessons_result.scalars().all()

        def is_time_conflict(lesson1, lesson2):
            return not (lesson1.end_time <= lesson2.start_time or lesson1.start_time >= lesson2.end_time)

        available_lessons = [
            {"id": available_lesson.id, "start_time": available_lesson.start_time, "end_time": available_lesson.end_time, "coach": coach.full_name}
            for available_lesson in available_lessons
            if all(not is_time_conflict(available_lesson, booked_lesson) for booked_lesson in booked_lessons)
        ]

        return available_lessons


async def reschedule_lesson(booked_lesson_id: int, new_lesson_id: int) -> bool:
    async with async_session() as session:

        result = await session.execute(
            select(Lesson).where(Lesson.id == new_lesson_id)
        )
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
                update(Lesson)
                .where(Lesson.id == current_lesson_id)
                .values(available=True)
            )

        await session.execute(
                update(Lesson)
                .where(Lesson.id == new_lesson_id)
                .values(available=False)
            )

        await session.commit()

        return True


async def get_coach_name(booked_lesson_id: int) -> str:
    async with async_session() as session:
        # Check if the new lesson is available
        result = await session.execute(
            select(Coach.full_name).join(BookedLesson, BookedLesson.id_coach == Coach.id)
            .where(BookedLesson.id == booked_lesson_id)
        )

        return result.scalar()
