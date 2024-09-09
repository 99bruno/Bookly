from app.database.models import async_session
from app.database.models import Manager, Event
from sqlalchemy import select


async def check_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Manager).where(Manager.tg_id == tg_id))
        if user:
            return True
        else:
            return False


async def check_admin(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Manager).where(Manager.tg_id == tg_id))
        if user.admin:
            return True
        else:
            return False
