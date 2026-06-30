from fastapi.testclient import TestClient
from app.main import app
from app.models.model import User
from app.database.setup_db import get_db
from testing.setup_db_test import override_get_db, TestingSessionLocal
from uuid import uuid4

import bcrypt

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def help_create_admin():
    db = TestingSessionLocal()
    try:
        unique = str(uuid4())[:8]
        password = "12345"

        password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()
        user = User(
            username=f"admin_{unique}",
            email=f"admin{unique}@gmail.com",
            password_hash=password_hash,
            role="admin"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        response = client.post(
            "/login",
            data={
                "username": user.username,
                "password": password
            }
        )
        return {
            "access_token": response.json()["access_token"],
            "user_id": user.id_user,
            "username": user.username
        }
    finally:
        db.close()

def help_get_token():
    unique = str(uuid4())[:8]

    client.post(
        "/register",
        json= {
            "username": f"test_{unique}",
            "email": f"test{unique}@gmail.com",
            "password": "123456j",
        }
    )

    response = client.post(
        "/login",
        data= {
            "username": f"test_{unique}",
            "password": "123456j"
        }
    )

    return response.json()["access_token"]

def help_create_cart():
    token = help_get_token()

    headers = {
        "Authorization" : f"Bearer {token}"
    }

    response = client.post(
        "/cart/product",
        json={
            "id_product": 2,
            "quantity": 1
        },headers=headers
    )

    data = response.json()

    return {
        "id_product": data["id_product"],
        "token": token
    }
