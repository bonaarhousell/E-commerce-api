from fastapi.testclient import TestClient
from app.main import app
from app.database.setup_db import get_db
from testing.setup_db_test import override_get_db
from testing.helpers import help_create_admin, help_get_token
from uuid import uuid4

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_product_role_admin():
    data_admin = help_create_admin()
    headers = {
        "Authorization": f"Bearer {data_admin['access_token']}"
    }
    unique = str(uuid4())[:8]
    response = client.post(
        "/product",
        json={
            "name_product": f"Book_{unique}",
            "price_product": 760000,
            "stock": 5,
            "category_product": "Book",
        },headers=headers
    )
    
    assert response.status_code == 201
    assert response.json()["message"] == "Product created"

def test_create_product_role_user():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    unique = str(uuid4())[:8]
    response = client.post(
        "/product",
        json={
            "name_product": f"Book_{unique}",
            "price_product": 760000,
            "stock": 5,
            "category_product": "Book",
        },headers=headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only admin can create product"


def test_get_product():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get(
        "/product",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0
    assert "id_product" in data[0]
    assert "name_product" in data[0]
    assert "price_product" in data[0]
    assert "category_product" in data[0]
    assert "stock" in data[0]

def test_get_product_filter_category():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get(
        f"/product?category=Fashion",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0
    for product in data:
        assert product["category_product"] == "Fashion"

def test_get_detail_product_():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get(
        f"/product/{3}",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id_product"] == 3

    assert len(data) > 0
    assert "name_product" in data
    assert "price_product" in data
    assert "category_product" in data
    assert "stock" in data

def test_remove_product_role_admin():
    data_admin = help_create_admin()
    headers = {
        "Authorization": f"Bearer {data_admin['access_token']}"
    }
    unique = str(uuid4())[:8]
    new_product_response = client.post(
        "/product",
        json={
            "name_product": f"Hoodie_{unique}",
            "price_product": 280000,
            "stock": 12,
            "category_product": "Fashion",
        },headers=headers
    ) 

    assert new_product_response.status_code == 201

    new_product = new_product_response.json()
    response = client.delete(
        f"/product/{new_product['id_product']}",
        headers=headers
    )
    assert response.status_code == 200

    assert response.json()["message"] == "Product Successfully removed"
    assert response.json()["id_product"] == new_product["id_product"]


def test_remove_product_role_user():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(
        "/product/2",headers=headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only admin can remove the product"

def test_update_product_role_admin():
    data_admin = help_create_admin()
    headers = {
        "Authorization": f"Bearer {data_admin['access_token']}"
    }

    unique = str(uuid4())[:8]
    product = client.post(
        "/product",
        json={
            "name_product": f"Hoodie_{unique}",
            "price_product": 280000,
            "stock": 12,
            "category_product": "Fashion"
        },headers=headers
    )

    data_product = product.json()

    update_product = client.put(
        f"/product/{data_product['id_product']}",
        json={
            "name_product": f"Book_{unique}",
            "price_product": 750000,
            "category_product": "Book",
            "stock": 18
        },headers=headers
    )

    assert update_product.status_code == 200

    data = update_product.json()

    assert data["message"] == "product Succesfully updated"
    assert data["new_product_name"] == f"Book_{unique}"
    assert data["id_product"] == data_product["id_product"]

def test_update_product_role_user():
    token = help_get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    unique = str(uuid4())[:8]
    update_product = client.put(
        "/product/2",
        json={
            "name_product": f"Book_{unique}",
            "price_product": 750000,
            "category_product": "Book",
            "stock": 18
        },headers=headers
    )

    assert update_product.status_code == 403
    assert update_product.json()["detail"] == "Only admin can update the product"

def test_update_product_stock():
    data_admin = help_create_admin()
    headers = {
        "Authorization": f"Bearer {data_admin['access_token']}"
    }

    unique = str(uuid4())[:8]
    product = client.post(
        "/product",
        json={
            "name_product": f"Hoodie_{unique}",
            "price_product": 280000,
            "stock": 12,
            "category_product": "Fashion"
        },headers=headers
    )

    data_product = product.json()
    new_product_stock = client.put(
        f"/product/stock/{data_product['id_product']}",
        json={
            "stock": 80
        },headers=headers
    )

    assert new_product_stock.status_code == 200

    data = new_product_stock.json()
    assert data["message"] == "Product Succesfully updated"
    assert data["new_product_stock"] == 80
    assert data["id_product"] == data_product["id_product"]