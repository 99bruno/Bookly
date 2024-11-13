from app.database.models import Event, Manager, async_session
from sqlalchemy import select


async def check_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Manager).where(Manager.tg_id == tg_id))
        if user:
            return True
        else:
            return False


async def check_user_have_chat_id_registered(tg_id, chat_id):
    async with async_session() as session:
        user = await session.scalar(select(Manager).where(Manager.tg_id == tg_id))
        if user.chat_id:
            return True
        else:
            user.chat_id = chat_id
            await session.commit()
            return False


async def check_admin(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Manager).where(Manager.tg_id == tg_id))
        if user.admin:
            return True
        else:
            return False


async def get_admins():
    async with async_session() as session:
        admins = await session.execute(
            select(Manager.chat_id).where(Manager.admin == True)
        )
        return admins.scalars().all()
