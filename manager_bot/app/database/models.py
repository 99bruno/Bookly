from datetime import date, datetime
from sqlalchemy import BigInteger, String, DATE, ForeignKey, DATETIME, BOOLEAN, Integer, Column
from typing import Optional, List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="sqlite+aiosqlite:///app/database/db.sqlite3")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Manager(Base):
    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)


class Dancer(Base):
    __tablename__ = 'dancers'
    id = Column(Integer, primary_key=True)
    tg_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    tg_username = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    name = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=True)
    full_name = Column(String(101), nullable=True)

    couple_id = Column(Integer, ForeignKey('couples.id'))

    couples = relationship('Couple', foreign_keys=[couple_id])


class Couple(Base):
    __tablename__ = 'couples'
    id = Column(Integer, primary_key=True)
    id_dancer1 = Column(Integer, ForeignKey('dancers.id'))
    id_dancer2 = Column(Integer, ForeignKey('dancers.id'))

    dancer1 = relationship('Dancer', foreign_keys=[id_dancer1])
    dancer2 = relationship('Dancer', foreign_keys=[id_dancer2])

    booked_lessons: Mapped[List["BookedLesson"]] = relationship("BookedLesson", back_populates="couple",
                                                                cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events" # Table name

    id: Mapped[int] = mapped_column(primary_key=True) # Event id
    name: Mapped[str] = mapped_column(String(50)) # Event name
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # Event description
    date_start: Mapped[date] = mapped_column(DATE()) # Event start date
    date_end: Mapped[date] = mapped_column(DATE()) # Event end date
    id_schedule: Mapped[int] = mapped_column(ForeignKey('schedule_events.id'))# Schedule id

    id_manager: Mapped[int] = mapped_column(ForeignKey('managers.id')) # Manager id

    coaches: Mapped[List["Coach"]] = relationship("Coach", back_populates="event", cascade="all, delete-orphan")# Coaches of the event
    schedule: Mapped["ScheduleEvent"] = relationship("ScheduleEvent", back_populates="events") # Schedule of the event


class ScheduleEvent(Base):
    __tablename__ = "schedule_events"  # Table name

    id: Mapped[int] = mapped_column(primary_key=True) # Schedule id
    dates: Mapped[str] = mapped_column(String(500)) # List of dates
    start_time: Mapped[str] = mapped_column(String(500)) # List of start times
    end_time: Mapped[str] = mapped_column(String(500)) # List of end times
    lesson_duration: Mapped[int] = mapped_column(Integer()) # Lesson duration in minutes
    breaks: Mapped[str] = mapped_column(String(1000)) # List of breaks
    full_schedule: Mapped[str] = mapped_column(String(1000)) # Full schedule

    events: Mapped[List["Event"]] = relationship("Event", back_populates="schedule", cascade="all, delete-orphan") # Events with this schedule


class Coach(Base):
    __tablename__ = "coaches"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    full_name: Mapped[str] = mapped_column(String(101))
    id_event: Mapped[int] = mapped_column(ForeignKey('events.id'))
    price: Mapped[int] = mapped_column(Integer())
    currency: Mapped[str] = mapped_column(ForeignKey('currencies.id'))
    program: Mapped[bool] = mapped_column(BOOLEAN())  # True - Latin, False - Ballroom
    dates: Mapped[str] = mapped_column(String(500))

    event: Mapped["Event"] = relationship("Event", back_populates="coaches")
    lessons: Mapped[List["Lesson"]] = relationship("Lesson", back_populates="coach", cascade="all, delete-orphan")
    booked_lessons: Mapped[List["BookedLesson"]] = relationship("BookedLesson", back_populates="coach",
                                                                cascade="all, delete-orphan")


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_coach: Mapped[int] = mapped_column(ForeignKey('coaches.id'))
    available: Mapped[bool] = mapped_column(BOOLEAN())
    date: Mapped[date] = mapped_column(DATE())
    start_time: Mapped[datetime] = mapped_column(DATETIME())
    end_time: Mapped[datetime] = mapped_column(DATETIME())
    price: Mapped[int] = mapped_column(Integer())
    currency: Mapped[str] = mapped_column(ForeignKey('currencies.id'))
    program: Mapped[bool] = mapped_column(BOOLEAN())  # True - Latin, False - Ballroom

    coach: Mapped["Coach"] = relationship("Coach", back_populates="lessons")
    booked_lessons: Mapped[List["BookedLesson"]] = relationship("BookedLesson", back_populates="lesson",
                                                                cascade="all, delete-orphan")


class BookedLesson(Base):
    __tablename__ = "booked_lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_lesson: Mapped[int] = mapped_column(ForeignKey('lessons.id'))
    id_coach: Mapped[int] = mapped_column(ForeignKey('coaches.id'))
    id_couple: Mapped[int] = mapped_column(ForeignKey('couples.id'))
    paid: Mapped[bool] = mapped_column(BOOLEAN())

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="booked_lessons")
    coach: Mapped["Coach"] = relationship("Coach", back_populates="booked_lessons")
    couple: Mapped["Couple"] = relationship("Couple", back_populates="booked_lessons")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)