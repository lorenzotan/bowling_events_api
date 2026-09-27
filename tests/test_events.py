from datetime import date

from sqlmodel import Session

from app.db.models import Event

LOCATION_PAYLOAD = {
    "name": "Cal Bowl",
    "address": "2500 E Carson St",
    "city": "Lakewood",
    "state": "CA",
    "zip": "90712",
}

EVENT_PAYLOAD = {
    "name": "Summer League",
    "category": "league",
}


def test_create_event_without_location(client):
    response = client.post("/api/v1/events/", json=EVENT_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == EVENT_PAYLOAD["name"]
    assert data["location_id"] is None


def test_create_event_with_location(client):
    location_id = client.post(
        "/api/v1/locations/", json=LOCATION_PAYLOAD
    ).json()["id"]

    response = client.post(
        "/api/v1/events/",
        json={**EVENT_PAYLOAD, "location_id": location_id},
    )

    assert response.status_code == 200
    assert response.json()["location_id"] == location_id


def test_read_events_empty(client):
    response = client.get("/api/v1/events/")

    assert response.status_code == 200
    assert response.json() == []


def test_read_events_returns_created(client):
    client.post("/api/v1/events/", json=EVENT_PAYLOAD)

    response = client.get("/api/v1/events/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == EVENT_PAYLOAD["name"]


def test_read_events_embeds_location(client):
    location = client.post("/api/v1/locations/", json=LOCATION_PAYLOAD).json()
    client.post(
        "/api/v1/events/",
        json={**EVENT_PAYLOAD, "location_id": location["id"]},
    )

    data = client.get("/api/v1/events/").json()

    assert data[0]["location_id"] == location["id"]
    assert data[0]["location"] == location


def test_read_events_without_location_has_null_location(client):
    client.post("/api/v1/events/", json=EVENT_PAYLOAD)

    data = client.get("/api/v1/events/").json()

    assert data[0]["location"] is None


def test_read_events_sorted_by_start_date(client, engine):
    # Inserted directly: POST /events/ takes the table model as its body,
    # which SQLModel doesn't validate, so date strings aren't parsed.
    with Session(engine) as session:
        for name, start_date in [
            ("Late", date(2026, 11, 1)),
            ("Early", date(2026, 10, 1)),
            ("Middle", date(2026, 10, 15)),
        ]:
            session.add(
                Event(name=name, category="league", start_date=start_date)
            )
        session.commit()

    data = client.get("/api/v1/events/").json()

    assert [event["name"] for event in data] == ["Early", "Middle", "Late"]
