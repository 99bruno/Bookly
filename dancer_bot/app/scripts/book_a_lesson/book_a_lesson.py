def concatenate_couples(couples: list) -> list[str]:
    return [" - ".join([couple["dancer1_full_name"], couple["dancer2_full_name"]]) for couple in couples]


def format_couple(couples):
    return [f"• Пара {idx+1}: "+couple for idx, couple in enumerate(couples)]


def format_lesson_info(lesson_info: dict, template: str) -> str:
    dates = '\n'.join(lesson_info['dates'])
    total_sum = lesson_info['total_sum']

    return template.format(dates, total_sum)
