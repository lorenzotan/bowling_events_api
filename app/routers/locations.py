from decouple import config
from fastapi import APIRouter, FastAPI
from sqlmodel import (
    create_engine,
    select,
    Session
)
from ..db.models import Location


app = FastAPI()
router = APIRouter()

postgres_url = config("DATABASE_URL")
engine = create_engine(postgres_url, echo=True)

@router.get("/locations/")
async def read_locations():
    with Session(engine) as session:
        # session.get(Location, id)
        locations = session.exec(select(Location)).all()
        return locations

"""
JSON Response Template
{
    id: <location_id>
    name: <bowling_house_name>
    address: <address>
    city: <city>
    state: <state>
    zip: <zip_code>
}
"""

app.include_router(router)