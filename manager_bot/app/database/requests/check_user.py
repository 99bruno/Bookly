from app.database.models import async_session
from app.database.models import Manager, Event
from sqlalchemy import select


async def check_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Manager).where(Manager.tg_id == tg_id))
        print("Fine", user)
        if user:
            return True
        else:
            return False
