from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.json().get("message") == "Welcome to my new api!!!!"

def test_create_user():
    res = client.post(
        "/api/users",
        json={"email": "test2@email.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
