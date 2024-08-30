from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import async_session, Event

async def update_event(update_data: dict, event_id: int=1):
    async with async_session() as session:
        async with session.begin():

            result = await session.execute(select(Event).where(Event.id == event_id))
            event = result.scalar_one_or_none()

            if event:

                for key, value in update_data.items():
                    setattr(event, key, value)
                session.add(event)
                await session.commit()
                return event
            else:
                return None


async def get_event_info(event_id: int=1):
    async with async_session() as session:
        result = await session.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()

        if event:
            return event
        else:
            return False


async def get_description(event_id: int=1):
    async with async_session() as session:
        result = await session.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()

        if event:
            return list(event.description)
        else:
            return ["The event does not exist"]
