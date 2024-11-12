from app.database.models import Couple, Dancer, async_session
from sqlalchemy import select, update
from sqlalchemy.orm import aliased


async def check_user_registered_by_phone(phone_number: int) -> int | bool:
    async with async_session() as session:
        dancer = await session.scalar(
            select(Dancer).where(Dancer.phone == phone_number)
        )

        if dancer:
            return dancer.id
        else:
            return False


async def check_couple_exists(dancer1_id: int, dancer2_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(Couple).where(
                (Couple.id_dancer1 == dancer1_id) & (Couple.id_dancer2 == dancer2_id)
                | (Couple.id_dancer1 == dancer2_id) & (Couple.id_dancer2 == dancer1_id)
            )
        )
        couple = result.scalars().first()

        return couple is not None


async def add_couple(dancer1_id: int, dancer2_id: int) -> None:
    async with async_session() as session:
        couple = Couple(id_dancer1=dancer1_id, id_dancer2=dancer2_id)
        session.add(couple)
        await session.commit()


async def add_user(
    tg_id: int,
    tg_username: str,
    phone_number: int,
    name: str,
    surname: str,
    full_name: str,
    chat_id: int = 0,
) -> None:
    async with async_session() as session:
        try:
            if tg_id is not None:
                dancer = Dancer(
                    tg_id=tg_id,
                    tg_username=tg_username,
                    phone=phone_number,
                    name=name,
                    surname=surname,
                    full_name=full_name,
                    chat_id=chat_id,
                )
            else:
                dancer = Dancer(
                    tg_username="TBA",
                    phone=phone_number,
                    name=name,
                    surname=surname,
                    full_name=full_name,
                )
        except:
            pass
        session.add(dancer)
        await session.commit()
