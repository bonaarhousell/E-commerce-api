from fastapi.testclient import TestClient
from app.main import app
from app.database.setup_db import get_db
from testing.setup_db_test import override_get_db
from testing.helpers  import help_get_token

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_checkout_product():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/checkout/7",
        json={
            "quantity": 2
        },headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Checkout Successfully"
    assert data["status"] == "paid"
    assert "id_order" in data

def test_checkout_product_invalid_stock():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(
        "/checkout/7",
        json={
            "quantity": 1000
        },headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Product not have enough stock"

def test_checkout_product_invalid_id():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    #il test with id 1200
    response = client.post(
        "/checkout/1200",
        json={
            "quantity": 2
        },headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_checkout_product_from_cart():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    client.post(
        "/cart/product",
        json={
            "id_product": 6,
            "quantity": 1
        },headers=headers
    )
    response = client.post(
        "/checkout",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Checkout Successfully"
    assert data["status"] == "paid"
    assert "id_order" in data

def test_checkout_product_from_cart_invalid_stock():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    client.post(
        "/cart/product",
        json={
            "id_product": 6,
            "quantity": 999
        },headers=headers
    )

    response = client.post(
        "/checkout",headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Stock is insufficient"


def test_checkout_product_without_cart():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/checkout",headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"

def test_checkout_requires_authentication():
    response = client.post(
        "/checkout",
        json={"quantity": 2}
    )

    assert response.status_code == 401