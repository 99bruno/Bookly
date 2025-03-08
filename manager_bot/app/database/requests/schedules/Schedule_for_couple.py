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
    Currency
)
from sqlalchemy import select
from sqlalchemy.orm import aliased

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from sqlalchemy.sql.sqltypes import Concatenable


def draw_centered_text(c, text, y_position, max_width, initial_font_size, font_name="Helvetica-Bold"):
    font_size = initial_font_size
    text_width = c.stringWidth(text, font_name, font_size)

    while text_width > max_width and font_size > 1:
        font_size -= 1
        text_width = c.stringWidth(text, font_name, font_size)

    c.setFont(font_name, font_size)
    c.drawString((max_width - text_width) / 2, y_position, text)


async def get_lesson_for_each_couple() -> dict:
    c = canvas.Canvas("app/database/couple_schedule.pdf", pagesize=A4)
    width, height = A4
    y_position = height - 20


    try:
        async with async_session() as session:

            camp = await session.execute(select(Event.name))
            camp = camp.scalar_one_or_none()

            text = f"Couple Schedule for {camp.strip()}"
            draw_centered_text(c, text, y_position - 40, width, 50)
            c.line(0, y_position - 70, width * mm, y_position - 70)
            y_position -= 100

            Dancer1 = aliased(Dancer, name="Dancer1")
            Dancer2 = aliased(Dancer, name="Dancer2")

            result = await session.execute(
                select(BookedLesson.id_couple, (Dancer1.full_name + " & " + Dancer2.full_name).label("couple_name"), Lesson.date.label("date"), Lesson.start_time.label("start_time"), Lesson.end_time, Lesson.program, Coach.full_name, Lesson.price, Currency.name, BookedLesson.paid,
                        (Dancer1.phone).label("dancer1_phone"), (Dancer2.phone).label("dancer2_phone")
                       )
                .outerjoin(Couple, BookedLesson.id_couple == Couple.id)
                .outerjoin(Dancer1, Couple.id_dancer1 == Dancer1.id)
                .outerjoin(Dancer2, Couple.id_dancer2 == Dancer2.id)
                .outerjoin(Lesson, BookedLesson.id_lesson == Lesson.id)
                .outerjoin(Coach, Lesson.id_coach == Coach.id)
                .outerjoin(Currency, Lesson.currency == Currency.id)
                .order_by(Dancer1.full_name, "date", "start_time")
            )
            lessons = result.fetchall()

            id_couple = 0
            current_date = 0
            money = {"USD": 0, "EUR": 0, "UAH": 0, "GBP": 0}

            for idx, lesson in enumerate(lessons):
                if lesson[0] != id_couple:
                    c.setFillColor(colors.black)
                    id_couple = lesson[0]
                    if idx != 0:
                        c.drawString(15 * mm, y_position-5, f"Total unpaid price: "
                                                          f"{'' if not money['USD'] else str(money['USD']) + ' USD'} "
                                                          f"{'' if not money['EUR'] else str(money['EUR']) + ' EUR'} "
                                                          f"{'' if not money['UAH'] else str(money['UAH']) + ' UAH'} "
                                                          f"{'' if not money['GBP'] else str(money['GBP']) + ' GBP'} "
                                     )
                        c.setFont("Helvetica-Bold", 18)
                        c.line(0, y_position - 30, width * mm, y_position - 30)
                        c.drawString(10 * mm, y_position - 70, f"{lesson[1].strip()}")
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(10 * mm, y_position - 90, f"+{lesson[10]} & +{lesson[11]}")
                        c.setFont("Helvetica-Bold", 18)
                        y_position -= 120

                    else:
                        c.setFont("Helvetica-Bold", 18)
                        c.drawString(10 * mm, y_position-10, f"{lesson[1].strip()}")
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(10 * mm, y_position - 30, f"+{lesson[10]} & +{lesson[11]}")
                        c.setFont("Helvetica-Bold", 18)
                        y_position -= 60
                    money = {"USD": 0, "EUR": 0, "UAH": 0, "GBP": 0}

                if lesson[2] != current_date:
                    current_date = lesson[2]
                    c.setFont("Helvetica-Bold", 12)
                    c.setFillColor(colors.black)
                    c.drawString(15 * mm, y_position, f"{lesson[2].strftime('%d-%m-%Y')}")
                    y_position -= 20

                c.setFont("Helvetica", 12)
                # if lesson[9]:
                #     c.setFillColor(colors.green)
                # else:
                #     c.setFillColor(colors.red)
                money[lesson[8]] += lesson[7]
                c.drawString(20 * mm, y_position, f"• {lesson[3].strftime('%H:%M')}-{lesson[4].strftime('%H:%M')} | {lesson[6]} | {lesson[7]} {lesson[8]}")
                y_position -= 15
                if y_position < 50:
                    c.showPage()
                    y_position = height - 20

            c.setFillColor(colors.black)
            c.drawString(15 * mm, y_position - 5, f"Total unpaid price: "
                                                  f"{'' if not money['USD'] else str(money['USD']) + ' USD'} "
                                                  f"{'' if not money['EUR'] else str(money['EUR']) + ' EUR'} "
                                                  f"{'' if not money['UAH'] else str(money['UAH']) + ' UAH'} "
                                                  f"{'' if not money['GBP'] else str(money['GBP']) + ' GBP'} ")

            c.save()

    except Exception as e:
        print(e)


text_format = """
{0}
"""

