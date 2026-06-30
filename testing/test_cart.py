from fastapi.testclient import TestClient
from app.main import app
from app.database.setup_db import get_db
from testing.setup_db_test import override_get_db
from testing.helpers import help_get_token, help_create_cart


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_add_product_to_cart():
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

    assert response.status_code == 201

    data = response.json()
    
    assert data["message"] == "product successfully add to cart"
    assert data["id_product"] == 2

def test_get_cart():
    token = help_get_token()

    headers = {
        "Authorization" : f"Bearer {token}"
    }

    client.post(
        "/cart/product",
        json={
            "id_product": 2,
            "quantity": 1
        },headers=headers
    )

    response = client.get(
        "/cart",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["id_product"] == 2
    assert data["items"][0]["quantity"] == 1
    assert data["items"][0]["subtotal"] == 650000

def test_remove_product_from_cart():
    data_cart = help_create_cart()
    headers = {
        "Authorization": f"Bearer {data_cart['token']}"
    }
    response = client.delete(
        f"/cart/product/{data_cart['id_product']}",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "product removed from cart"
    assert data["id_product"] == data_cart["id_product"]

def test_remove_product_invalid_id():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    client.post(
        "/cart/product",
        json={
            "id_product": 2,
            "quantity": 1
        },headers=headers
    )

    response = client.delete(
        f"/cart/product/{99}",headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found in cart"


def test_update_product_in_cart():
    data_cart = help_create_cart()
    headers = {
        "Authorization": f"Bearer {data_cart['token']}"
    }
    response = client.put(
        f"/cart/product/{data_cart['id_product']}",
        json={
            "new_quantity": 5
        },headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Cart updated"
    assert data["id_product"] == data_cart["id_product"]
    assert data["quantity"] == 5

def test_update_product_cart_insufficient_stock():
    data_cart = help_create_cart()
    headers = {
        "Authorization": f"Bearer {data_cart['token']}"
    }
    response = client.put(
        f"/cart/product/{data_cart['id_product']}",
        json={
            "new_quantity": 999
        },headers=headers
    )

    assert response.status_code == 400

    assert response.json()["detail"] == "Insufficient stock"