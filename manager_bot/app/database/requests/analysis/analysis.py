from app.database.models import Coach, Dancer, async_session, BookedLesson, Couple, Currency
from sqlalchemy import select, update
from sqlalchemy import text
from sqlalchemy import func, select, case
from app.database.models import Coach, BookedLesson, Lesson
from sqlalchemy.orm import aliased


async def get_coach_lessons_summary():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    Lesson.id_coach.label('coach_id'),
                    Coach.full_name,
                    func.count(func.distinct(BookedLesson.id)).label('booked_lessons_count'),
                    func.count(func.distinct(Lesson.id)).label('total_lessons_count'),
                    func.count(func.distinct(case((Lesson.available == False, Lesson.id)))).label('unavailable_lessons_count'),
                    func.count(func.distinct(case((Lesson.available == True, Lesson.id)))).label('available_lessons_count')
                )
                .outerjoin(BookedLesson, Lesson.id == BookedLesson.id_lesson)
                .join(Coach, Coach.id == Lesson.id_coach)
                .group_by(Lesson.id_coach, Coach.full_name)
            )
            return result.all()


async def get_lessons_counts():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    (select(func.count()).select_from(BookedLesson)).label('booked_lessons_count'),
                    (select(func.count()).select_from(Lesson)).label('total_lessons_count'),
                    (select(func.count()).select_from(Lesson).where(Lesson.available == False)).label('unavailable_lessons_count'),
                    (select(func.count()).select_from(Lesson).where(Lesson.available == True)).label('available_lessons_count')
                )
            )
            return result.one()


async def get_available_lessons_summary():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    Coach.full_name,
                    func.count(Lesson.id).label('total_available_lessons'),
                    Lesson.date.label('available_date')
                )
                .where(Lesson.available == True)
                .join(Coach, Coach.id == Lesson.id_coach)
                .group_by(Lesson.id_coach, Lesson.date)
                .order_by(Lesson.id_coach, Lesson.date)
            )
            return result.all()


query = """
SELECT 
    currencies.name,
    SUM(l.price) AS total_sum,                            -- Загальна сума (вільні + заброньовані)
    SUM(CASE WHEN bl.id IS NOT NULL THEN l.price ELSE 0 END) AS booked_sum, -- Сума лише заброньованих
    SUM(CASE WHEN bl.paid = TRUE THEN l.price ELSE 0 END) AS paid_sum       -- Сума лише оплачених
FROM lessons l
LEFT JOIN booked_lessons bl ON l.id = bl.id_lesson        -- Приєднуємо інформацію про бронювання
JOIN currencies ON currencies.id = l.currency            -- Приєднуємо інформацію про валюту
WHERE l.available = TRUE OR bl.id IS NOT NULL             -- Враховуємо лише вільні або заброньовані уроки
GROUP BY l.currency                                       -- Групуємо за валютою
ORDER BY l.currency;                                      -- Сортуємо за валютою
"""

async def get_lessons_financial_summary():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(text(query))
            return result.fetchall()