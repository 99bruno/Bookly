from sqlalchemy import select, update
from app.database.models import async_session, Dancer, Couple
from sqlalchemy.orm import aliased


async def check_user_registered(tg_id: int) -> int | bool:
    async with async_session() as session:
        dancer = await session.scalar(select(Dancer).where(Dancer.tg_id == tg_id))

        if dancer:
            return dancer.id
        else:
            return False


async def add_user(tg_id: int, tg_username: str, phone_number: int, name: str, surname: str, full_name: str) -> None:
    async with async_session() as session:
        try:
            if tg_id is not None:
                dancer = Dancer(tg_id=tg_id, tg_username=tg_username, phone=phone_number, name=name, surname=surname,
                                full_name=full_name)
            else:
                dancer = Dancer(tg_username="TBA", phone=phone_number, name=name, surname=surname, full_name=full_name)
        except:
            pass
        session.add(dancer)
        await session.commit()


async def check_couple_registered(dancer_id: int) -> list | bool:
    async with async_session() as session:
        Dancer1 = aliased(Dancer)
        Dancer2 = aliased(Dancer)

        result = await session.execute(
            select(Couple, Dancer1.full_name.label('dancer1_full_name'), Dancer2.full_name.label('dancer2_full_name'))
            .join(Dancer1, Couple.id_dancer1 == Dancer1.id)
            .join(Dancer2, Couple.id_dancer2 == Dancer2.id)
            .where(
                (Couple.id_dancer1 == dancer_id) | (Couple.id_dancer2 == dancer_id)
            )
        )
        couples_info = result.fetchall()

        if not couples_info:  # Check if the result is empty
            return False

        return [
            {
                "couple_id": couple.id,
                "dancer1_full_name": dancer1_full_name,
                "dancer2_full_name": dancer2_full_name
            }
            for couple, dancer1_full_name, dancer2_full_name in couples_info]


async def check_user_registered_by_phone(phone_number: int) -> int | bool:
    async with async_session() as session:
        dancer = await session.scalar(select(Dancer).where(Dancer.phone == phone_number))

        if dancer:
            return dancer.id
        else:
            return False


async def add_couple(dancer1_id: int, dancer2_id: int) -> None:
    async with async_session() as session:
        couple = Couple(id_dancer1=dancer1_id, id_dancer2=dancer2_id)
        session.add(couple)
        await session.commit()


async def check_couple_exists(dancer1_id: int, dancer2_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(Couple).where(
                (Couple.id_dancer1 == dancer1_id) & (Couple.id_dancer2 == dancer2_id) |
                (Couple.id_dancer1 == dancer2_id) & (Couple.id_dancer2 == dancer1_id)
            )
        )
        couple = result.scalars().first()

        return couple is not None


async def update_dancer_info(user_id: int, username: str, tg_id: int) -> None:
    async with async_session() as session:
        await session.execute(
            update(Dancer)
            .where(Dancer.id == user_id)
            .values(tg_username=username, tg_id=tg_id)
        )
        await session.commit()
