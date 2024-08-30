import ast


async def coach_added_message_unpack(data: dict, template: str) -> str:
    return template.format(
        data["name"]+" "+data["surname"], data["price"]+" "+data["currency"],
        "Latin" if data["program"] == True else "Ballroom",
        ", ".join(data["dates"]),
        ", ".join(data["full_schedule"]),
        )


