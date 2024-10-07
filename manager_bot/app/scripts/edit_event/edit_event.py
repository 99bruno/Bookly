async def edit_camp_info(update_data):
    from app.database.requests.edit_event import update_event
    from datetime import date

    event_id = 1

    if list(update_data.keys())[0] == "date":
        start_date = update_data["date"].split("-")[0].split(".")
        end_date = update_data["date"].split("-")[1].split(".")

        update_data["date_start"] = date(int(start_date[-1]), int(start_date[-2]), int(start_date[-3]))
        update_data["date_end"] = date(int(end_date[-1]), int(end_date[-2]), int(end_date[-3]))
        del update_data["date"]

    updated_event = await update_event(event_id, update_data)
    if updated_event:
        print("Event updated successfully")
    else:
        print("Event not found")