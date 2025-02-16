import ast
from datetime import datetime, timedelta
from sqlalchemy import and_

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
                    print(coach[1], date_obj)

                    result = await session.execute(
                        select(Lesson.available, Lesson.start_time, Lesson.end_time, BookedLesson.paid,
                               Dancer1.full_name.label("dancer1_name"), Dancer2.full_name.label("dancer2_name")
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
                                                                 is not None else '! Blocked !' if lesson[0] == False and lesson[4]
                                                                                                   is None else
                              ''}"
                              )
                             for lesson in lessons]))
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(20 * mm, y_position, f"{coach[1]} Schedule for {date}:")
                    y_position -= 5
                    for line in lesson_string.split("\n"):
                        c.setFont("Helvetica", 12)
                        c.setFillColor(colors.black)
                        if "! Blocked !" in line:
                            c.setFillColor(colors.red)
                        c.drawString(20 * mm, y_position, line)
                        y_position -= 15

                        if y_position < 50:  # Prevent writing beyond the page
                            c.showPage()
                            y_position = height - 20
                c.showPage()
                y_position = height - 20

            c.save()
    except Exception as e:
        print(e)


text_format = """
{0}
"""

