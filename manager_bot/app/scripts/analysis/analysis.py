from itertools import groupby
import datetime


async def analysis_booked_lessons_unpack(lessons: tuple) -> str:
    return (f"<b>Booked lessons:</b>\n\n"
            f"<blockquote>• {lessons[0]}/{lessons[1]-(lessons[2]-lessons[0])} ~ "
            f"{lessons[0]/(lessons[1]-(lessons[2]-lessons[0])) * 100:.1f}%</blockquote>\n\n"
            f"<span class='tg-spoiler'>Avaliable lessons: {lessons[3]}\n"
            f"Blocked lessons: {lessons[2]-lessons[0]}\n</span>"
            )


async def analysis_coaches_booking_rating_unpack(coaches: list) -> str:
    try:
        return ("<b>Coaches booking rating:</b>\n\n"
         "<blockquote>") + "\n".join(
            [
                f"{idx + 1}. {coach[1]}: {coach[2]}/{(coach[3] - (coach[4] - coach[2]))} ~ {coach[2] / (coach[3] - (coach[4] - coach[2])) * 100:.1f}%"
                for idx, coach in enumerate(sorted(coaches, key=lambda x: x[2] / x[3] if (x[3] - (x[4] - x[2])) == 0 else x[2] / (x[3] - (x[4] - x[2])), reverse=True)) if (coach[3] - (coach[4] - coach[2])) > 0]
        ) + "</blockquote>"

    except:
        print(coaches)


async def analysis_coaches_with_available_lessons_unpack(coaches: list) -> str:
    return ("<b>Coaches with available lessons:\n\n</b>" + "<blockquote>")+(
            "\n".join(
        [f"{idx+1}. {key} - {", ".join([f"{element[2].strftime("%d.%m")}({element[1]})" for element in group])}" for idx, (key, group) in enumerate(groupby(coaches, lambda coach: coach[0]))]
    ) + "</blockquote>"
    )


async def analysis_overall_income_unpack(income: list) -> str:
    return ("<b>Overall income:</b>\n\n"
            f"<blockquote>"
            f"{"\n".join([f"• {currency[2]}/{currency[1]} {currency[0]} ~ {currency[2]/currency[1] * 100:.1f}%" for currency in income])}"
            f"</blockquote>"
            f"\n\n<b>Paid lessons:</b>\n\n"
            f"<blockquote>"
            f"{"\n".join([f"• {currency[3]}/{currency[2]} {currency[0]} ~ {currency[3]/currency[2] * 100:.1f}%" for currency in income])}"
            "</blockquote>"
            )
