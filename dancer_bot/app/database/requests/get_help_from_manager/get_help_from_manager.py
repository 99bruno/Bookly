from app.database.models import Event, async_session
from sqlalchemy import select


async def get_event_info(event_id=1):
    async with async_session() as session:
        result = await session.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()

        if event:
            return event
        else:
            return False
