from sqlalchemy import select, delete, update
from app.database.models import async_session, Coach, Dancer

currency = ["EUR", "USD", "UAH", "GBP"]


async def check_user_registered(tg_id):
    async with async_session() as session:

        if await session.scalar(select(Dancer).where(Dancer.tg_id == tg_id)):
            return True
        else:
            return False


async def get_coaches_by_program(program_type: str):
    async with async_session() as session:
        result = await session.execute(
            select(Coach).where(Coach.program == (program_type == "Latin"))
        )
        coaches = result.scalars().all()

        if not coaches:
            return False

        return [
            {
                "id": coach.id,
                "fullname": coach.full_name,
                "price": str(coach.price) + " " + currency[coach.currency-1],
            }
            for coach in coaches
        ]


async def get_coach_info(coach_id: int) -> dict:
    async with async_session() as session:
        result = await session.execute(select(Coach).filter(Coach.id == coach_id))
        coach = result.scalars().first()

        if not coach:
            return False

        return {
            "coach_id": coach.id,
            "fullname": coach.full_name,
            "price": str(coach.price)+" "+currency[coach.currency-1],
            "dates": coach.dates,
            "program": "Latin" if coach.program else "Ballroom",
        }
