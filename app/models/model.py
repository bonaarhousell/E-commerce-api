from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.setup_db import Base, engine
from typing import List

class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str] = mapped_column(default="user", nullable=False)
    my_orders : Mapped[List["Order"]] = relationship(back_populates="user")
    my_carts : Mapped["Cart"] = relationship(back_populates="user", uselist=False)

class Product(Base):
    __tablename__ = "products"

    id_product: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_product: Mapped[str]
    price_product: Mapped[int]
    stock: Mapped[int]
    category_product: Mapped[str]
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="products")
    cart_items: Mapped[List["CartItem"]] = relationship( back_populates="products")

class Cart(Base):
    __tablename__ = "carts"

    id_cart : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id_user"))
    user : Mapped["User"] = relationship(back_populates="my_carts")
    cart_items : Mapped[List["CartItem"]] = relationship(back_populates="carts")

class CartItem(Base):
    __tablename__ = "cart_items"

    id_cart_item: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cart: Mapped[int] = mapped_column(ForeignKey("carts.id_cart"))
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id_product")) 
    quantity: Mapped[int]
    carts : Mapped["Cart"] = relationship( back_populates="cart_items")
    products : Mapped["Product"] = relationship( back_populates="cart_items")

class Order(Base):
    __tablename__ = "orders"

    id_order: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id_user"))
    total_price: Mapped[int]
    status: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="my_orders")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"

    id_order_item: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_order: Mapped[int] = mapped_column(ForeignKey("orders.id_order"))
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id_product"))
    quantity: Mapped[int]
    unit_price: Mapped[int]
    subtotal: Mapped[int]
    orders: Mapped["Order"] = relationship(back_populates="order_items")
    products: Mapped["Product"] = relationship(back_populates="order_items")

