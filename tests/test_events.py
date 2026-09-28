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


def test_create_event_parses_date_and_time(client):
    client.post(
        "/api/v1/events/",
        json={
            **EVENT_PAYLOAD,
            "start_date": "2026-10-06",
            "game_time": "18:30:00",
        },
    )

    data = client.get("/api/v1/events/").json()

    assert data[0]["start_date"] == "2026-10-06"
    assert data[0]["game_time"] == "18:30:00"


def test_create_event_missing_category_is_rejected(client):
    response = client.post("/api/v1/events/", json={"name": "No Category"})

    assert response.status_code == 422


def test_read_events_sorted_by_start_date(client):
    for name, start_date in [
        ("Late", "2026-11-01"),
        ("Early", "2026-10-01"),
        ("Middle", "2026-10-15"),
    ]:
        client.post(
            "/api/v1/events/",
            json={**EVENT_PAYLOAD, "name": name, "start_date": start_date},
        )

    data = client.get("/api/v1/events/").json()

    assert [event["name"] for event in data] == ["Early", "Middle", "Late"]
