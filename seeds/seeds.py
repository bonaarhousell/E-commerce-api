from sqlalchemy.orm import Session

from app.database.setup_db import SessionLocal
from app.models.model import Product, User

import bcrypt

def create_admin(db: Session):
    existing_admin = db.query(User).filter(
        User.username == "adminbon"
    ).first()

    if existing_admin:
        return
    password = "12345"
    password_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    user = User(
        username="adminbon",
        email="adminbon@gmail.com",
        password_hash=password_hash,
        role="admin"
    )
    db.add(user)

products = [
    {
        "name_product": "Mechanical Keyboard",
        "price_product": 650000,
        "stock": 20,
        "category_product": "Electronics",
    },
    {
        "name_product": "Wireless Mouse",
        "price_product": 250000,
        "stock": 35,
        "category_product": "Electronics",
    },
    {
        "name_product": "Gaming Headset",
        "price_product": 450000,
        "stock": 18,
        "category_product": "Electronics",
    },
    {
        "name_product": "27-inch Monitor",
        "price_product": 2500000,
        "stock": 10,
        "category_product": "Electronics",
    },
    {
        "name_product": "USB-C Charger",
        "price_product": 180000,
        "stock": 40,
        "category_product": "Electronics",
    },
    {
        "name_product": "Oversized Hoodie",
        "price_product": 275000,
        "stock": 30,
        "category_product": "Fashion",
    },
    {
        "name_product": "Running Shoes",
        "price_product": 850000,
        "stock": 15,
        "category_product": "Fashion",
    },
    {
        "name_product": "Denim Jacket",
        "price_product": 550000,
        "stock": 12,
        "category_product": "Fashion",
    },
    {
        "name_product": "Backpack",
        "price_product": 320000,
        "stock": 22,
        "category_product": "Fashion",
    },
    {
        "name_product": "Ceramic Coffee Mug",
        "price_product": 65000,
        "stock": 50,
        "category_product": "Home",
    },
    {
        "name_product": "Desk Lamp",
        "price_product": 180000,
        "stock": 16,
        "category_product": "Home",
    },
    {
        "name_product": "Office Chair",
        "price_product": 1750000,
        "stock": 8,
        "category_product": "Home",
    },
    {
        "name_product": "Notebook A5",
        "price_product": 30000,
        "stock": 120,
        "category_product": "Stationery",
    },
    {
        "name_product": "Ballpoint Pen",
        "price_product": 10000,
        "stock": 250,
        "category_product": "Stationery",
    },
    {
        "name_product": "Sticky Notes",
        "price_product": 15000,
        "stock": 100,
        "category_product": "Stationery",
    }
]

db = SessionLocal()

create_admin(db)

for product in products:
    exist_product = db.query(Product).filter(
        Product.name_product == product["name_product"]
    ).first()

    if exist_product:
        continue

    db.add(
        Product(
            name_product=product["name_product"],
            price_product=product["price_product"],
            stock=product["stock"],
            category_product=product["category_product"]
        )
    )

db.commit()
db.close()