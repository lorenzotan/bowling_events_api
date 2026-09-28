from datetime import date, time

from decouple import config
from models import Event, Location
from sqlmodel import (
    Session,
    create_engine,
    select,
)

postgres_url = config("DATABASE_URL")

engine = create_engine(postgres_url, echo=True)

# SQLModel.metadata.create_all(engine)


def create_locations() -> None:
    with Session(engine) as session:
        locations = [
            Location(
                name="Cal Bowl",
                address="2500 E Carson St",
                city="Lakewood",
                state="CA",
                zip="90712",
            ),
            Location(
                name="Bowlero Cerritos",
                address="18811 Carmenita Rd",
                city="Cerritos",
                state="CA",
                zip="90703",
            ),
            Location(
                name="Bowlero Fullerton",
                address="1501 S Lemon St",
                city="Fullerton",
                state="CA",
                zip="92832",
            ),
            Location(
                name="Concourse Bowling Center",
                address="3364 E La Palma Ave",
                city="Anaheim",
                state="CA",
                zip="92806",
            ),
            Location(
                name="Westminster Lanes",
                address="6471 Westminster Blvd",
                city="Westminster",
                state="CA",
                zip="92683",
            ),
        ]

        for location in locations:
            session.add(location)

        session.commit()


# Sample events; "location" is a seeded location name.
SAMPLE_EVENTS = [
    {
        "name": "Fall Classic Mixed League",
        "category": "league",
        "location": "Cal Bowl",
        "start_date": date(2026, 10, 6),
        "end_date": date(2027, 3, 30),
        "game_day": "Tuesday",
        "game_time": time(18, 30),
    },
    {
        "name": "Southland Scratch Open",
        "category": "tournament",
        "location": "Bowlero Fullerton",
        "start_date": date(2026, 10, 10),
        "end_date": date(2026, 10, 10),
        "game_day": "Saturday",
        "game_time": time(10, 0),
    },
    {
        "name": "Thursday Night Trios",
        "category": "league",
        "location": "Bowlero Cerritos",
        "start_date": date(2026, 10, 15),
        "end_date": date(2027, 4, 22),
        "game_day": "Thursday",
        "game_time": time(19, 0),
    },
    {
        "name": "Anaheim Handicap Doubles",
        "category": "tournament",
        "location": "Concourse Bowling Center",
        "start_date": date(2026, 10, 24),
        "end_date": date(2026, 10, 25),
        "game_day": "Saturday",
        "game_time": time(9, 0),
    },
    {
        "name": "Senior Sunday League",
        "category": "league",
        "location": "Westminster Lanes",
        "start_date": date(2026, 11, 1),
        "end_date": date(2027, 5, 2),
        "game_day": "Sunday",
        "game_time": time(13, 0),
    },
    {
        "name": "Holiday No-Tap Sweeper",
        "category": "tournament",
        "location": "Cal Bowl",
        "start_date": date(2026, 12, 12),
        "end_date": date(2026, 12, 12),
        "game_day": "Saturday",
        "game_time": time(12, 0),
    },
]


def create_events() -> None:
    """Seed sample events, linked to the seeded locations by name."""
    with Session(engine) as session:
        location_ids = {
            location.name: location.id
            for location in session.exec(select(Location)).all()
        }
        for sample in SAMPLE_EVENTS:
            fields = {k: v for k, v in sample.items() if k != "location"}
            location_id = location_ids[sample["location"]]
            session.add(Event(**fields, location_id=location_id))

        session.commit()


def is_seeded() -> bool:
    """Whether a previous run already seeded the database."""
    with Session(engine) as session:
        return session.exec(select(Location)).first() is not None


if __name__ == "__main__":
    if not is_seeded():
        create_locations()
        create_events()
