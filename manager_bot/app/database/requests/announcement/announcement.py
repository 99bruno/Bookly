from app.database.models import Coach, Dancer, async_session, BookedLesson, Couple
from sqlalchemy import select, update
from sqlalchemy.orm import aliased


async def get_all_user_id() -> list[int]:
    async with async_session() as session:

        result = await session.execute(select(Dancer.tg_id).where((Dancer.tg_id != "") & (Dancer.tg_id != 1)))
        dancers = result.scalars().all()

        return (dancer for dancer in dancers)


async def get_all_coaches() -> list:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Coach))
            coaches = result.scalars().all()

            coaches_dict = [
                {
                    "id": coach.id,
                    "name": coach.full_name
                }
                for coach in coaches
            ]

            return coaches_dict


async def get_user_id_by_coach_id(coach_id: int) -> list[int]:
    async with async_session() as session:
        async with session.begin():
            result1 = await session.execute(
                select(Dancer.tg_id)
                .join(Couple, Couple.id_dancer1 == Dancer.id)
                .join(BookedLesson, BookedLesson.id_couple == Couple.id)
                .where(BookedLesson.id_coach == coach_id)
            )
            result2 = await session.execute(
                select(Dancer.tg_id)
                .join(Couple, Couple.id_dancer2 == Dancer.id)
                .join(BookedLesson, BookedLesson.id_couple == Couple.id)
                .where(BookedLesson.id_coach == coach_id)
            )
            dancers1 = result1.scalars().all()
            dancers2 = result2.scalars().all()
            return set(list(dancers1) + list(dancers2))