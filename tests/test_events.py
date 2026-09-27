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
