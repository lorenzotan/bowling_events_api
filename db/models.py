from datetime import date, time
from sqlmodel import (
    Field,
    Relationship,
    SQLModel
)


class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    address: str
    city: str
    state: str
    zip: str
    events: list['Event'] = Relationship(back_populates='location')


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: str
    start_date: date | None = None
    end_date: date | None = None
    game_day: str | None = None
    game_time: time | None = None
    registration_url: str | None = None
    location_id: int | None = Field(default=None, foreign_key='location.id')

    location: Location | None = Relationship(back_populates='events')
