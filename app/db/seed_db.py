from models import Location
from sqlmodel import (
    create_engine,
    Session,
    SQLModel,
)
from decouple import config

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
                zip="90712"
            ),
            Location(
                name="Bowlero Cerritos",
                address="18811 Carmenita Rd",
                city="Cerritos",
                state="CA",
                zip="90703"
            ),
            Location(
                name="Bowlero Fullerton",
                address="1501 S Lemon St",
                city="Fullerton",
                state="CA",
                zip="92832"
            ),
            Location(
                name="Concourse Bowling Center",
                address="3364 E La Palma Ave",
                city="Anaheim",
                state="CA",
                zip="92806"
            ),
            Location(
                name="Westminster Lanes",
                address="6471 Westminster Blvd",
                city="Westminster",
                state="CA",
                zip="92683"
            ),
        ]

        for location in locations:
            session.add(location)
        
        session.commit()


if __name__ == "__main__":
    create_locations()