from typing import List

from fastapi import APIRouter, FastAPI
from sqlmodel import Session, select

from app.db.database import engine
from app.db.models import Location

app = FastAPI()
router = APIRouter(prefix="/api/v1")


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
