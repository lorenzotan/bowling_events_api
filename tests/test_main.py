from fastapi.testclient import TestClient

from app.main import app  # Assuming your main FastAPI app is in app/main.py

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
