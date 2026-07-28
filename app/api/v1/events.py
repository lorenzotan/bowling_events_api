from typing import List

from fastapi import APIRouter, FastAPI
from sqlmodel import Session, select

from app.db.database import engine
from app.db.models import Event

app = FastAPI()
router = APIRouter(prefix="/api/v1")


@router.post("/events/")
async def write_event(event: Event):
    with Session(engine) as session:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event


@router.get("/events/", tags=["events"])
async def read_events() -> List[Event]:
    with Session(engine) as session:
        return session.exec(select(Event)).all()


"""
JSON Response Template
{
    "id": "<event_id>",
    "name": "<event_name>",
    "category": "<category league|tournament>",
    "start_date": "<start_date>",
    "end_date": "<end_date>",
    "game_day": "<game_day>",
    "game_time": "<game_time>",
    "registration_url": "<url>",
    "location": {
        "name": "<bowling_house_name>",
        "address": "<address>",
        "city": "<city>",
        "state": "<state>",
        "zip": "<zip_code>"
    }
}
"""

app.include_router(router)
