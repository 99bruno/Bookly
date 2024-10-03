from sqlalchemy import select
from sqlalchemy.orm import aliased
import pandas as pd
import numpy as np
import ast
from datetime import datetime, timedelta

from app.database.models import async_session, Lesson, BookedLesson, Couple, Dancer, Coach, ScheduleEvent, Payment, Change

async def fetch_lessons_with_full_info():
    Dancer1 = aliased(Dancer, name='Dancer1')
    Dancer2 = aliased(Dancer, name='Dancer2')

    async with async_session() as session:
        result = await session.execute(
            select(
                Lesson.id,
                Lesson.id_coach,
                Lesson.available,
                Lesson.date,
                Lesson.start_time,
                Lesson.end_time,
                Lesson.price,
                Lesson.currency,
                Lesson.program,
                BookedLesson.id,
                BookedLesson.id_lesson,
                BookedLesson.id_coach,
                BookedLesson.id_couple,
                BookedLesson.paid,
                Coach.full_name.label('coach_name'),
                Dancer1.full_name.label('dancer1_name'),
                Dancer2.full_name.label('dancer2_name')
            )
            .outerjoin(BookedLesson, Lesson.id == BookedLesson.id_lesson)
            .outerjoin(Couple, BookedLesson.id_couple == Couple.id)
            .outerjoin(Dancer1, Couple.id_dancer1 == Dancer1.id)
            .outerjoin(Dancer2, Couple.id_dancer2 == Dancer2.id)
            .join(Coach, Lesson.id_coach == Coach.id)
        )
        lessons = result.fetchall()

        schedule = await session.execute(select(ScheduleEvent.full_schedule).where(ScheduleEvent.id == 1))
        schedule = schedule.scalar_one_or_none()

        indexes_1 = ast.literal_eval(schedule)
        indexes_2 = ["07:45-08:30", "08:30-09:15", "09:15-10:00", "10:00-10:45", "11:00-11:45", "11:45-12:30", "12:30-13:15", "13:30-14:15", "14:15-15:00", "15:00-15:45", "16:00-16:45", "16:45-17:30"]

        dancers = await session.execute(select(Dancer.full_name, Dancer.tg_username, Dancer.phone))
        dancers = dancers.fetchall()

        result = await session.execute(select(Payment.time_of_payment,
                                              Payment.manager_nickname,
                                              Payment.couple_name,
                                              Payment.coach_name, Payment.lesson_date, Payment.price, Payment.currency))
        payments = result.fetchall()

        result = await session.execute(select(Change.time_of_change,
                                                Change.dancer_username,
                                                Change.couple_name,
                                                Change.coach_name, Change.lesson_date, Change.lesson_id, Change.reason
                                              ))

        changes = result.fetchall()

        result = await session.execute(select(Coach.id, Coach.full_name, Coach.dates))

        coaches = result.fetchall()

    coaches = pd.DataFrame(coaches)

    # Convert to Pandas DataFrame
    df = pd.DataFrame(lessons, columns=[
        'id', 'id_coach', 'available', 'date', 'start_time', 'end_time', 'price', 'currency', 'program',
        'id', 'id_lesson', 'id_coach', 'id_couple', 'paid', 'coach_name', 'dancer1_name', 'dancer2_name'
    ])

    dates = df[(df["date"] == df["date"].unique()[0]) & (df["coach_name"] == df["coach_name"].unique()[0])].shape[0]

    dates_np = np.empty(dates)
    dates_np[:] = np.nan

    dates_error = ['2024-12-02', '2024-12-03']

    with pd.ExcelWriter('app/database/schedule.xlsx') as writer:
        pd.DataFrame(dancers).to_excel(writer, sheet_name="dancers")
        pd.DataFrame(payments).to_excel(writer, sheet_name="payments")
        pd.DataFrame(changes).to_excel(writer, sheet_name="cancelations")

        df_dict = dict()
        for date in df["date"].unique():
            print(date)

            for coach in df["coach_name"].unique():
                if date.strftime('%d.%m.%Y') in ast.literal_eval(list(coaches[coaches["full_name"] == coach]["dates"])[0]):
                    df_test = df[(df["date"] == date) & (df["coach_name"] == coach)][["available", 'dancer1_name', 'dancer2_name', 'paid']]
                    df_test["couple"] = df_test["dancer1_name"] + " & " + df_test["dancer2_name"]
                    df_dict[coach] = dates_np if not len(df_test["couple"].values) else df_test["couple"].values
                    df_dict[f"{coach.split()[0]} Payment Status"] = ["✅"if paid is True else "❌" for paid in df_test["paid"].values]
            try:
                print([[ds, len(df_dict[ds])] for ds in df_dict])
                pd.DataFrame(df_dict, index=(indexes_1 if date.strftime('%Y-%m-%d') in
                                                          dates_error else indexes_2)).to_excel(writer,
                                                                                                sheet_name=date.strftime('%d-%m-%Y'))
            except Exception as e:
                print(f"Error - {e}")
                print(coach)