async def get_days_between_dates(start_date, end_date):
    from datetime import datetime, timedelta

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    days_list = []
    current_date = start_date
    while current_date <= end_date:
        days_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return days_list


async def get_days_of_the_camp():
    from app.database.requests.edit_event import get_event_info

    event_info = await get_event_info()

    return await get_days_between_dates(event_info.date_start, event_info.date_end)
