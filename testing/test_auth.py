from fastapi.testclient import TestClient
from app.main import app
from app.database.setup_db import get_db
from testing.setup_db_test import override_get_db
from uuid import uuid4

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register_and_login_success():
    unique = str(uuid4())[:8]
    register = client.post(
        "/register",
        json={
            "username": f"user_{unique}",
            "email": f"user{unique}@gmail.com",
            "password": "123456"
        }
    )

    assert register.status_code == 201

    response = client.post(
        "/login",
        data={
            "username": f"user_{unique}",
            "password": "123456"
        }
    )
    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


def test_login_wrong_password():
    unique = str(uuid4())[:8]
    client.post(
        "/register",
        json={
            "username": f"user_{unique}",
            "email": f"user_{unique}@gmail.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": f"user_{unique}",
            "password": "wrong password"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid Password"