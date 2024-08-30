from app.database.models import async_session
from app.database.models import Coach, Event, Lesson, BookedLesson

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def add_or_update_event(event_data):
    async with async_session() as session:
        # Check if the event exists
        result = await session.execute(select(Event).where(Event.id == event_data['id']))
        event = result.scalar_one_or_none()

        if event:
            # Event exists, delete related data
            await delete_related_data(session, event.id)
            # Update event
            for key, value in event_data.items():
                setattr(event, key, value)
            session.add(event)
        else:
            # Add new event
            new_event = Event(**event_data)
            session.add(new_event)

        await session.commit()


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
