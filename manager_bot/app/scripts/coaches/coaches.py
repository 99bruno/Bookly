import ast

currency = ['USD', 'EUR', 'UAH', 'GBP']


def coaches_unpack_info(coaches_info, coaches_list_message):
    return coaches_list_message.format(
        "\n".join([f"{idx + 1}. {coach['coach']}" for idx, coach in enumerate(coaches_info)]))


def coach_unpack_info(coach_info, coach_info_message):
    return coach_info_message.format(f"• Full name: {coach_info['coach']}\n"
                                     f"• Program: {'Latin' if coach_info['program'] else 'Ballroom'}\n"
                                     f"• Price: {coach_info['price']} {currency[coach_info['currency'] - 1]}\n"
                                     f"• Dates: {", ".join(ast.literal_eval(coach_info['dates']))}"
                                     f"• Lesson restrictions: {coach_info['lesson_restrictions']}")


def coach_unpack_info_for_edit(coach_info, coach_info_message):
    return coach_info_message.format(f"• Name: {coach_info['name']}\n• Surname: {coach_info['surname']}\n"
                                     f"• Program: {'Latin' if coach_info['program'] else 'Ballroom'}\n"
                                     f"• Price: {coach_info['price']} {currency[coach_info['currency'] - 1]}\n"
                                     f"• Dates: {", ".join(ast.literal_eval(coach_info['dates']))}"
                                     f"• Lesson restrictions: {coach_info['lesson_restrictions']}")


def coach_view_schedule_unpack(lessons, template):

    return template.format(lessons[0],
                           "\n".join(
                               [f"• <b>{lesson['time']} </b> - "
                                f"{(lesson['couple']['couples_name'] + ' ✅' 
                                    if lesson['couple']["paid_status"] else lesson['couple']['couples_name'] + ' ❌') 
                                if lesson['available'] is False else ''}\n"


                                for lesson in lessons[1]

                                ]

                           )
                           )
