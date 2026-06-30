from fastapi.testclient import TestClient
from app.main import app
from app.database.setup_db import get_db
from testing.setup_db_test import override_get_db
from testing.helpers import help_get_token

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_get_order():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    client.post(
        "/checkout/7",
        json={
            "quantity": 1
        },headers=headers
    )

    response = client.get(
        "/order",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]["status"] == "paid"
    assert "id_order" in data[0]

def test_get_order_without_checkout():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/order",headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order Empty"

def test_get_detail_order():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    checkout = client.post(
        "/checkout/2",
        json={
            "quantity": 1
        },headers=headers
    )

    checkout_data = checkout.json()
    response = client.get(
        f"/order/{checkout_data['id_order']}",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id_order"] == checkout_data["id_order"]
    assert data["total_price"] == checkout_data["total_price"]
    assert data["status"] == "paid"
    assert "item" in data

def test_get_detail_order_invalid_id():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    client.post(
        "/checkout/2",
        json={
            "quantity": 1
        },headers=headers
    )

    #il test with id_order equal to 999
    response = client.get(
        "/order/999",headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"