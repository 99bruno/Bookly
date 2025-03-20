import ast
from datetime import datetime, timedelta
from sqlalchemy import and_, distinct

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
    Event,
    ScheduleEvent,
    async_session,
)
from sqlalchemy import select
from sqlalchemy.orm import aliased

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm



async def get_dates_of_event() -> list[datetime]:
    async with async_session() as session:
        result = await session.execute(select(ScheduleEvent.dates).where(ScheduleEvent.id == 1))
        dates = result.scalar_one_or_none()

        return [datetime.strptime(date, "%d.%m.%Y") for date in [date.lstrip().strip("'") for date in dates[2:-2].split(",")]]

def draw_centered_text(c, text, y_position, max_width, initial_font_size, font_name="Helvetica-Bold"):
    font_size = initial_font_size
    text_width = c.stringWidth(text, font_name, font_size)

    while text_width > max_width and font_size > 1:
        font_size -= 1
        text_width = c.stringWidth(text, font_name, font_size)

    c.setFont(font_name, font_size)
    c.drawString((max_width - text_width) / 2, y_position, text)


async def get_lesson_for_each_coach() -> dict:
    c = canvas.Canvas("app/database/coach_schedule.pdf", pagesize=A4)
    width, height = A4
    y_position = height - 20

    try:
        async with async_session() as session:
            Dancer1 = aliased(Dancer, name="Dancer1")
            Dancer2 = aliased(Dancer, name="Dancer2")
            result = await session.execute(
                select(Coach.id, Coach.full_name, Coach.dates, Coach.program).order_by(Coach.full_name)
            )
            camp = await session.execute(select(Event.name))
            camp = camp.scalar_one_or_none()

            coaches = result.fetchall()
            text = f"Coach Schedule for {camp.strip()}"
            draw_centered_text(c, text, y_position - 40, width, 50)
            y_position -= 120

            for line in [f"{idx+1}. {coach[1]}" for idx, coach in enumerate(coaches)]:
                c.setFont("Helvetica", 12)
                c.setFillColor(colors.black)
                c.drawString(10 * mm, y_position, line)
                y_position -= 15

                if y_position < 50:
                    c.showPage()
                    y_position = height - 20

            if y_position != height - 20:
                c.showPage()
                y_position = height - 20

            for coach in coaches:
                text = f"{coach[1]}"
                draw_centered_text(c, text, y_position - 20, width, 30)
                y_position -= 60
                for date in ast.literal_eval(coach[2]):
                    date_obj = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")

                    result = await session.execute(
                        select(Lesson.available, Lesson.start_time, Lesson.end_time, BookedLesson.paid,
                               Dancer1.full_name.label("dancer1_name"), Dancer2.full_name.label("dancer2_name"), Lesson.program, Lesson.date
                               )
                        .outerjoin(BookedLesson, Lesson.id == BookedLesson.id_lesson)
                        .outerjoin(Couple, BookedLesson.id_couple == Couple.id)
                        .outerjoin(Dancer1, Couple.id_dancer1 == Dancer1.id)
                        .outerjoin(Dancer2, Couple.id_dancer2 == Dancer2.id)
                        .where(
                            and_(Lesson.date == date_obj, Lesson.id_coach == coach[0])
                        )
                    )
                    lessons = result.fetchall()

                    lesson_string = text_format.format(
                        "\n".join(
                            [(f"• {lesson[1].strftime('%H:%M')}-{lesson[2].strftime('%H:%M')}: "
                              f"{f'{lesson[4]} & {lesson[5]}' if lesson[0] == False and lesson[4]
                                                                 is not None else 'No lesson' if lesson[0] == False and lesson[4]
                                                                                                   is None else
                              ''}"
                              )
                             for lesson in lessons]))
                    c.setFont("Helvetica-Bold", 12)
                    c.setFillColor(colors.black)
                    c.drawString(20 * mm, y_position, f"{coach[1]} Schedule for {date}:")
                    y_position -= 5
                    for line, lesson, idx in zip(lesson_string.split("\n"), lessons, range(len(lessons))):
                        if lesson[6] and lesson[7].strftime("%d-%m") in ["27-03", "28-03", "29-03"] and lesson[1].strftime("%H:%M") in ["17:30", "18:15"]:
                            c.setFillColor(colors.red)
                            if lesson[1].strftime("%H:%M") == "17:30":

                                c.drawString(20 * mm, y_position, f"• 17:15-17:45: Latin Lecture")
                                y_position -= 15
                                c.drawString(20 * mm, y_position, f"• 17:45-18:15: Latin Lecture")
                                y_position -= 15
                            else:
                                c.drawString(20 * mm, y_position, f"• 18:00-18:30: Latin Lecture")
                                y_position -= 15
                                c.drawString(20 * mm, y_position, f"• 18:30-19:00: Latin Lecture")
                                y_position -= 15

                        elif not lesson[6] and lesson[7].strftime("%d-%m") in ["27-03", "28-03", "29-03"] and lesson[1].strftime("%H:%M") in ["11:15", "12:00"]:
                            c.setFillColor(colors.red)
                            if lesson[1].strftime("%H:%M") == "11:15":
                                c.drawString(20 * mm, y_position, f"• 11:00-11:30: Ballroom Lecture")
                                y_position -= 15
                                c.drawString(20 * mm, y_position, f"• 11:30-12:00: Ballroom Lecture")
                                y_position -= 15
                            else:
                                c.drawString(20 * mm, y_position, f"• 12:00-12:30: Ballroom Lecture")
                                y_position -= 15
                                c.drawString(20 * mm, y_position, f"• 12:30-13:00: Ballroom Lecture")
                                y_position -= 15


                        c.setFont("Helvetica", 12)
                        c.setFillColor(colors.black)
                        if "No lesson" in line:
                            c.setFillColor(colors.blue)
                        c.drawString(20 * mm, y_position, line)
                        y_position -= 15

                        if lesson[1] != lessons[idx - 1][2] and idx != 0:
                            c.setFillColor(colors.green)
                            c.drawString(20 * mm, y_position,
                                         f"• {round((lesson[1] - lessons[idx-1][2]).total_seconds() / 60)} min Break")
                            y_position -= 15

                        if y_position < 50:  # Prevent writing beyond the page
                            c.showPage()
                            y_position = height - 20
                c.showPage()
                y_position = height - 20

            c.save()
    except Exception as e:
        print("Error", e)


text_format = """
{0}
"""


async def get_lesson_for_each_coach_for_date(date: str) -> None:
    date_time = datetime.strptime(date, "%Y-%m-%d")
    print(date_time)
    c = canvas.Canvas(f"app/database/coach_schedule_{date}.pdf", pagesize=A4)
    width, height = A4
    y_position = height - 20


    try:
        async with async_session() as session:
            Dancer1 = aliased(Dancer, name="Dancer1")
            Dancer2 = aliased(Dancer, name="Dancer2")
            result = await session.execute(
                select(distinct(Lesson.id_coach), Coach.full_name)
                .join(Lesson, Lesson.id_coach == Coach.id)
                .where(Lesson.date == date)
            )

            camp = await session.execute(select(Event.name))
            camp = camp.scalar_one_or_none()

            coaches = result.fetchall()
            print(coaches)
            text = f"Coach Schedule for {camp.strip()} on {date}"
            draw_centered_text(c, text, y_position - 40, width, 50)
            y_position -= 120

            for line in [f"{idx+1}. {coach[1]}" for idx, coach in enumerate(coaches)]:
                c.setFont("Helvetica", 12)
                c.setFillColor(colors.black)
                c.drawString(10 * mm, y_position, line)
                y_position -= 15

                if y_position < 50:
                    c.showPage()
                    y_position = height - 20

            if y_position != height - 20:
                c.showPage()
                y_position = height - 20

            for coach in coaches:
                text = f"{coach[1]}"
                draw_centered_text(c, text, y_position - 20, width, 30)
                y_position -= 60


                result = await session.execute(
                    select(Lesson.available, Lesson.start_time, Lesson.end_time, BookedLesson.paid,
                           Dancer1.full_name.label("dancer1_name"), Dancer2.full_name.label("dancer2_name"),
                           Lesson.program, Lesson.date
                           )
                    .outerjoin(BookedLesson, Lesson.id == BookedLesson.id_lesson)
                    .outerjoin(Couple, BookedLesson.id_couple == Couple.id)
                    .outerjoin(Dancer1, Couple.id_dancer1 == Dancer1.id)
                    .outerjoin(Dancer2, Couple.id_dancer2 == Dancer2.id)
                    .where(
                        and_(Lesson.date == date, Lesson.id_coach == coach[0])
                    )
                )
                lessons = result.fetchall()

                lesson_string = text_format.format(
                    "\n".join(
                        [(f"• {lesson[1].strftime('%H:%M')}-{lesson[2].
                        
                        strftime('%H:%M')}: "
                          f"{f'{lesson[4]} & {lesson[5]}' if lesson[0] == False and lesson[4]
                                                             is not None else 'No lesson' if lesson[0] == False and lesson[4]
                                                                                               is None else
                          ''}"
                          )
                         for lesson in lessons]))


                c.setFont("Helvetica-Bold", 12)

                c.drawString(20 * mm, y_position, f"{coach[1]} Schedule for {date}:")


                y_position -= 5

                for line, lesson, idx in zip(lesson_string.split("\n"), lessons, range(len(lessons))):
                    if lesson[6] and lesson[7].strftime("%d-%m") in ["27-03", "28-03", "29-03"] and lesson[1].strftime(
                            "%H:%M") in ["17:30", "18:15"]:
                        c.setFillColor(colors.red)
                        if lesson[1].strftime("%H:%M") == "17:30":

                            c.drawString(20 * mm, y_position, f"• 17:15-17:45: Latin Lecture")
                            y_position -= 15
                            c.drawString(20 * mm, y_position, f"• 17:45-18:15: Latin Lecture")
                            y_position -= 15
                        else:
                            c.drawString(20 * mm, y_position, f"• 18:00-18:30: Latin Lecture")
                            y_position -= 15
                            c.drawString(20 * mm, y_position, f"• 18:30-19:00: Latin Lecture")
                            y_position -= 15

                    elif not lesson[6] and lesson[7].strftime("%d-%m") in ["27-03", "28-03", "29-03"] and lesson[
                        1].strftime("%H:%M") in ["11:15", "12:00"]:
                        c.setFillColor(colors.red)
                        if lesson[1].strftime("%H:%M") == "11:15":
                            c.drawString(20 * mm, y_position, f"• 11:00-11:30: Ballroom Lecture")
                            y_position -= 15
                            c.drawString(20 * mm, y_position, f"• 11:30-12:00: Ballroom Lecture")
                            y_position -= 15
                        else:
                            c.drawString(20 * mm, y_position, f"• 12:00-12:30: Ballroom Lecture")
                            y_position -= 15
                            c.drawString(20 * mm, y_position, f"• 12:30-13:00: Ballroom Lecture")
                            y_position -= 15


                    c.setFont("Helvetica", 12)
                    c.setFillColor(colors.black)
                    if "No lesson" in line:
                        c.setFillColor(colors.blue)
                    line.split(" & ")
                    c.drawString(20 * mm, y_position, line)
                    y_position -= 15

                    if lesson[1] != lessons[idx-1][2] and idx != 0:
                        c.setFillColor(colors.green)
                        c.drawString(20 * mm, y_position, f"• {round((lesson[1] - lessons[idx-1][2]).total_seconds() / 60)} min Break")
                        y_position -= 15

                    if y_position < 50:
                        c.showPage()
                        y_position = height - 20

                c.showPage()
                y_position = height - 20

            c.save()
    except Exception as e:
        print(e)

    return None


