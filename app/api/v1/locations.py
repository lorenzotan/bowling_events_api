from decouple import config
from fastapi import APIRouter, FastAPI
from sqlmodel import (
    create_engine,
    select,
    Session
)
from typing import List
from app.db.models import Location


app = FastAPI()
router = APIRouter(prefix="/api/v1")

postgres_url = config("DATABASE_URL")
engine = create_engine(postgres_url, echo=True)


@router.post("/locations/")
async def write_locations(location: Location):
    with Session(engine) as session:
        session.add(location)
        session.commit()
        session.refresh(location)

        return location


@router.get("/locations/")
async def read_locations() -> List[Location]:
    with Session(engine) as session:
        return session.exec(select(Location)).all()

"""
JSON Response Template
{
    "id": "<location_id>",
    "name": "<bowling_house_name>",
    "address": "<address>",
    "city": "<city>",
    "state": "<state>",
    "zip": "<zip_code>"
}
"""

app.include_router(router)
