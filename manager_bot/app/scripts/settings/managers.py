async def remove_managers_msg_unpack(data: list[dict], template:str):
    return template.format(
        '\n'.join([f"{idx+1}. {manager['username']}" for idx, manager in enumerate(data)])
    )