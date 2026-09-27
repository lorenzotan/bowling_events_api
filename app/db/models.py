from datetime import date, time

from sqlmodel import Field, Relationship, SQLModel


class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    address: str
    city: str
    state: str
    zip: str
    events: list["Event"] = Relationship(back_populates="location")


class EventBase(SQLModel):
    """Fields shared by the Event table and its API response model."""

    name: str
    category: str
    start_date: date | None = None
    end_date: date | None = None
    game_day: str | None = None
    game_time: time | None = None
    registration_url: str | None = None
    location_id: int | None = Field(default=None, foreign_key="location.id")


class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    location: Location | None = Relationship(back_populates="events")


class EventPublic(EventBase):
    """Event as returned by GET /events/, with its location embedded."""

    id: int
    location: Location | None = None
