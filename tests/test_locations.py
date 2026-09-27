LOCATION_PAYLOAD = {
    "name": "Cal Bowl",
    "address": "2500 E Carson St",
    "city": "Lakewood",
    "state": "CA",
    "zip": "90712",
}


def test_create_location(client):
    response = client.post("/api/v1/locations/", json=LOCATION_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == LOCATION_PAYLOAD["name"]
    assert data["zip"] == LOCATION_PAYLOAD["zip"]


def test_read_locations_empty(client):
    response = client.get("/api/v1/locations/")

    assert response.status_code == 200
    assert response.json() == []


def test_read_locations_returns_created(client):
    client.post("/api/v1/locations/", json=LOCATION_PAYLOAD)

    response = client.get("/api/v1/locations/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == LOCATION_PAYLOAD["name"]
