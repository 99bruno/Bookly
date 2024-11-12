import ast
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from app.database.models import (
    BookedLesson,
    Change,
    Coach,
    Couple,
    Dancer,
    Lesson,
    Payment,
    ScheduleEvent,
    async_session,
)
from sqlalchemy import select
from sqlalchemy.orm import aliased


async def fetch_lessons_with_full_info():
    Dancer1 = aliased(Dancer, name="Dancer1")
    Dancer2 = aliased(Dancer, name="Dancer2")

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
                Coach.full_name.label("coach_name"),
                Dancer1.full_name.label("dancer1_name"),
                Dancer2.full_name.label("dancer2_name"),
            )
            .outerjoin(BookedLesson, Lesson.id == BookedLesson.id_lesson)
            .outerjoin(Couple, BookedLesson.id_couple == Couple.id)
            .outerjoin(Dancer1, Couple.id_dancer1 == Dancer1.id)
            .outerjoin(Dancer2, Couple.id_dancer2 == Dancer2.id)
            .join(Coach, Lesson.id_coach == Coach.id)
        )
        lessons = result.fetchall()

        schedule = await session.execute(
            select(ScheduleEvent.full_schedule).where(ScheduleEvent.id == 1)
        )
        schedule = schedule.scalar_one_or_none()

        indexes_1 = ast.literal_eval(schedule)
        indexes_2 = [
            "07:45-08:30",
            "08:30-09:15",
            "09:15-10:00",
            "10:00-10:45",
            "11:00-11:45",
            "11:45-12:30",
            "12:30-13:15",
            "13:30-14:15",
            "14:15-15:00",
            "15:00-15:45",
            "16:00-16:45",
            "16:45-17:30",
        ]
        indexes_3 = [
            "07:45-08:30",
            "08:30-09:15",
            "09:15-10:00",
            "10:00-10:45",
            "10:45-11:30",
            "11:30-12:15",
            "12:15-13:00",
            "13:00-13:45",
            "14:00-14:45",
            "14:45-15:30",
            "15:30-16:15",
            "16:15-17:00"
        ]
        indexes_4 = [
            "07:45-08:30",
            "08:30-09:15",
            "09:15-10:00",
            "10:00-10:45",
            "11:00-11:45",
            "11:45-12:30",
            "12:30-13:15",
            "13:30-14:15",
            "14:15-15:00",
            "15:00-15:45",
            "16:00-16:45",
            "16:45-17:30",
            "17:30-18:15",
            "18:30-19:15",
            "19:15-20:00",
            "20:15-21:00",
            "21:00-21:45"
        ]

        dancers = await session.execute(
            select(Dancer.full_name, Dancer.tg_username, Dancer.phone)
        )
        dancers = dancers.fetchall()

        result = await session.execute(
            select(
                Payment.time_of_payment,
                Payment.manager_nickname,
                Payment.couple_name,
                Payment.coach_name,
                Payment.lesson_date,
                Payment.price,
                Payment.currency,
            )
        )
        payments = result.fetchall()

        result = await session.execute(
            select(
                Change.time_of_change,
                Change.dancer_username,
                Change.couple_name,
                Change.coach_name,
                Change.lesson_date,
                Change.lesson_id,
                Change.reason,
            )
        )

        changes = result.fetchall()

        result = await session.execute(select(Coach.id, Coach.full_name, Coach.dates))

        coaches = result.fetchall()

    coaches = pd.DataFrame(coaches)

    # Convert to Pandas DataFrame
    df = pd.DataFrame(
        lessons,
        columns=[
            "id",
            "id_coach",
            "available",
            "date",
            "start_time",
            "end_time",
            "price",
            "currency",
            "program",
            "id",
            "id_lesson",
            "id_coach",
            "id_couple",
            "paid",
            "coach_name",
            "dancer1_name",
            "dancer2_name",
        ],
    )

    dates = df[
        (df["date"] == df["date"].unique()[0])
        & (df["coach_name"] == df["coach_name"].unique()[0])
    ].shape[0]
    print("dates", dates)

    dates_np_15 = np.empty(dates)
    dates_np_15[:] = np.nan

    dates_np_12 = np.empty(12)
    dates_np_12[:] = np.nan

    dates_np_8 = np.empty(8)
    dates_np_8[:] = np.nan

    dates_error = ["2024-12-02", "2024-12-03"]

    with pd.ExcelWriter("app/database/schedule.xlsx") as writer:
        pd.DataFrame(dancers).to_excel(writer, sheet_name="dancers")
        pd.DataFrame(payments).to_excel(writer, sheet_name="payments")
        pd.DataFrame(changes).to_excel(writer, sheet_name="cancelations")

        unique_dates = df["date"].unique()
        unique_coaches = df["coach_name"].unique()

        for date in unique_dates:
            df_dict = dict()
            date_str = date.strftime("%Y-%m-%d")
            date_str_dmy = date.strftime("%d-%m-%Y")

            for coach in unique_coaches:
                coach_dates = ast.literal_eval(
                    list(coaches[coaches["full_name"] == coach]["dates"])[0]
                )
                if date.strftime("%d.%m.%Y") in coach_dates:
                    df_test = df[(df["date"] == date) & (df["coach_name"] == coach)][
                        ["available", "dancer1_name", "dancer2_name", "paid"]
                    ]
                    df_test["couple"] = np.where(
                        (
                            df_test["dancer1_name"].isna()
                            & df_test["dancer2_name"].isna()
                            & ~df_test["available"]
                        ),
                        "Blocked ⚠️",
                        df_test["dancer1_name"] + " & " + df_test["dancer2_name"],
                    )
                    if date_str == "2024-12-06":
                        df_dict[coach] = (
                            dates_np_8
                            if df_test["couple"].empty
                            else df_test["couple"].values
                        )
                    elif date_str in dates_error:
                        df_dict[coach] = (
                            dates_np_15
                            if df_test["couple"].empty
                            else df_test["couple"].values
                        )
                    else:
                        df_dict[coach] = (
                            dates_np_12
                            if df_test["couple"].empty
                            else df_test["couple"].values
                        )

                    df_dict[f"{coach.split()[0]} Payment Status"] = [
                        "✅" if paid else "❌" for paid in df_test["paid"].values
                    ]

            try:
                if date_str == "2024-12-06":
                    pd.DataFrame(df_dict, index=indexes_3).to_excel(
                        writer, sheet_name=date_str_dmy
                    )
                elif date_str in ["2024-12-04", "2024-12-05"]:
                    pd.DataFrame(df_dict, index=indexes_4).to_excel(
                        writer, sheet_name=date_str_dmy
                    )
                else:
                    index = indexes_1 if date_str in dates_error else indexes_2
                    pd.DataFrame(df_dict, index=index).to_excel(
                        writer, sheet_name=date_str_dmy
                    )
            except Exception as e:
                print(f"Error processing date {date_str_dmy} - {e}")

# jdd: I'm not sure what this function does, but it seems to be a bit of a mess.