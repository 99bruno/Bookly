import json
from datetime import date, datetime
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Event, ScheduleEvent, async_session, Coach, Lesson, BookedLesson

async def add_event_with_schedule(dates: list,
                                  event_name: str,
                                  description: str,
                                  date_start: str,
                                  date_end: str,
                                  start_time: str,
                                  end_time: str,
                                  lesson_duration: int,
                                  breaks: str,
                                  full_schedule: str,
                                  manager_id: int) -> Event:
    async with async_session() as session:

        schedule = await add_or_update_schedule({"dates": json.dumps(str(dates)),
                                                 "start_time": start_time,
                                                 "end_time": end_time,
                                                 "lesson_duration": lesson_duration,
                                                 "breaks": json.dumps(breaks),
                                                 "full_schedule": json.dumps(full_schedule)},
                                                 session)

        event_info = {"name": event_name,
                      "description": description,
                      "date_start": datetime.strptime(date_start, '%d.%m.%Y'),
                      "date_end": datetime.strptime(date_end, '%d.%m.%Y'),
                      "id_schedule": 1,
                      "id_manager": manager_id}


        result = await session.execute(select(Event).where(Event.id == 1))
        event = result.scalar_one_or_none()

        if event:

            await delete_related_data(session, event.id)

            for key, value in event_info.items():
                setattr(event, key, value)
            session.add(event)
        else:
            # Add new event
            new_event = Event(**event_info)
            session.add(new_event)

        await session.commit()


async def add_or_update_schedule(schedule_info: dict, session) -> ScheduleEvent:
        # Check if the event exists
    result = await session.execute(select(ScheduleEvent).where(ScheduleEvent.id == 1))
    schedule = result.scalar_one_or_none()

    if schedule:

        for key, value in schedule_info.items():
            setattr(schedule, key, value)
        session.add(schedule)
    else:

        new_schedule = ScheduleEvent(**schedule_info)
        session.add(new_schedule)

    await session.commit()

    return schedule


async def delete_related_data(session: AsyncSession, event_id: int):
    # Delete related coaches, lessons and booked lessons
    result = await session.execute(select(Coach).where(Coach.id_event == event_id).options(
        selectinload(Coach.lessons).selectinload(Lesson.booked_lessons)))
    coaches = result.scalars().all()

    for coach in coaches:
        for lesson in coach.lessons:
            await session.execute(delete(BookedLesson).where(BookedLesson.id_lesson == lesson.id))
        await session.execute(delete(Lesson).where(Lesson.id_coach == coach.id))
    await session.execute(delete(Coach).where(Coach.id_event == event_id))


""" new_schedule = ScheduleEvent(
                dates=dates,
                start_time=start_time,
                end_time=end_time,
                lesson_duration=lesson_duration,
                breaks=breaks,
                full_schedule=full_schedule
            )

            session.add(new_schedule)
            await session.commit()
            await session.refresh(new_schedule)

            new_event = Event(
            name=event_name,
            description=description,
            date_start=date_start,
            date_end=date_end,
            id_schedule=new_schedule.id,
            id_manager=manager_id
            )

            session.add(new_event)
            await session.commit()
            await session.refresh(new_event)

            return new_event"""