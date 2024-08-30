import ast

async def check_camp_info_message_unpack(data: list, template: str) -> str:
    return template.format(
        data[0],
        "-".join([data[1].strftime("%d.%m.%Y"), data[2].strftime("%d.%m.%Y")]),
        data[3])



async def coaches_list_message_unpack(data: list[dict], template: str) -> str:
    return template.format(
        "\n".join(
            [
                f"{i + 1}. {coach['fullname']}"
                for i, coach in enumerate(data)
            ]
        )
    )


async def coach_info_message_unpack(data: dict, template: str) -> str:

    return template.format(
        data["fullname"],
        ", ".join(ast.literal_eval(data["dates"])),
        data["program"]
    )


async def coach_info_view_price_message_unpack(data: dict, template: str) -> str:
    return template.format(
        data["fullname"],
        data["dates"],
        data["program"],
        data["price"]
    )


async def coach_info_compare_price_message_unpack(data: list[dict], template: str, program: str) -> str:
    return template.format(
        program,
        "\n".join(
            [
                f"{i + 1}. {coach['fullname']} - {coach['price']}"
                for i, coach in enumerate(data)
            ]
        )
    )