async def edit_event_message_unpack(data, template: str) -> str:
    return template.format(
        data.name,
        data.date_start,
        data.date_end,
        data.description if data.description != "" else " ",
    )


async def format_string(data: list, template: str) -> str:
    return template.format(data)
