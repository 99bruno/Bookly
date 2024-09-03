from sqlalchemy import select
from app.database.models import async_session
from app.database.models import Manager


async def add_manager(tg_id: int, username: str):
    async with async_session() as session:
        async with session.begin():
            new_manager = Manager(tg_id=tg_id, tg_username=username, admin=False)
            session.add(new_manager)
            await session.commit()


async def add_admin(tg_id: int, username: str):
    async with async_session() as session:
        async with session.begin():
            new_manager = Manager(tg_id=tg_id, tg_username=username, admin=True)
            session.add(new_manager)
            await session.commit()


async def get_managers():
    async with async_session() as session:
        async with session.begin():
            managers = await session.execute(select(Manager).where(Manager.admin == False))
            return [{
                "id": manager.id,
                "username": manager.tg_username,
            }
                    for manager in managers.scalars().all()]


async def remove_manager(idx: int):
    async with async_session() as session:
        async with session.begin():
            manager = await session.get(Manager, idx)
            print(manager)
            if manager:
                await session.delete(manager)
                await session.commit()