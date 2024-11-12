from datetime import date, datetime, time, timedelta
from typing import List

from app.database.models import Coach, Lesson, async_session


async def add_coach_with_lessons(
    firstname: str, lastname: str, price: int, program: bool, dates: List[str]
):
    # Перетворення рядків дат на об'єкти date
    date_objects = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates]

    async with async_session() as session:
        async with session.begin():
            # Додавання нового тренера
            new_coach = Coach(
                firstname=firstname,
                lastname=lastname,
                id_event=1,
                price=price,
                program=program,
                dates=str(date_objects),
            )
            session.add(new_coach)
            await session.flush()  # Проміжне збереження для отримання ID тренера

            # Додавання уроків для нового тренера
            for lesson_date in date_objects:
                start_time = datetime.combine(
                    lesson_date, time(8, 0)
                )  # Початок першого уроку о 8:00
                while start_time.time() < time(20, 0):
                    end_time = start_time + timedelta(
                        minutes=45
                    )  # Урок триває 45 хвилин
                    if end_time.time() > time(20, 0):
                        break  # Завершити, якщо кінець уроку після 20:00

                    new_lesson = Lesson(
                        id_coach=new_coach.id,
                        available=True,
                        start_time=start_time,
                        end_time=end_time,
                        date=lesson_date,
                        price=price,
                        program=program,
                    )
                    session.add(new_lesson)

                    start_time = end_time + timedelta(
                        minutes=15 if (end_time.minute // 45) % 3 == 2 else 0
                    )
                    # Додаємо 15 хвилин перерви кожні 3 уроки

            # Збереження змін
            await session.commit()
