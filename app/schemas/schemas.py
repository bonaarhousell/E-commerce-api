from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class ProductCreate(BaseModel):
    name_product: str
    price_product: int
    category_product: Literal[
        "Electronics",
        "Food",
        "Book",
        "Stationery",
        "Fashion"
    ]
    stock: int

class ProductUpdate(BaseModel):
    name_product: str
    price_product: int
    category_product: Literal[
        "Electronics",
        "Food",
        "Book",
        "Stationery",
        "Fashion",
    ]
    stock: int

class ProductUpdateStock(BaseModel):
    stock: int

class ProductResponse(BaseModel):
    id_product: int
    name_product: str
    price_product: int
    category_product: str
    stock: int

class ProductDetailResponse(BaseModel):
    id_product: int
    name_product: str
    price_product: int
    category_product: str
    stock: int
    product_sold: int

class AddProductToCart(BaseModel):
    id_product: int
    quantity: int = Field(gt=0)

class UpdateCartItem(BaseModel):
    new_quantity: int = Field(gt=0)

class CartItemResponse(BaseModel):
    id_product: int
    name_product: str
    quantity: int
    subtotal: int

class CartResponse(BaseModel):
    items : list[CartItemResponse]
    total_cart_price: int

class OrderResponse(BaseModel):
    id_order: int
    total_price: int
    status: str

class OrderItemResponse(BaseModel):
    id_product: int
    name_product: str
    quantity: int
    unit_price: int
    subtotal: int    

class OrderItemDetailResponse(BaseModel):
    id_order: int
    total_price: int
    status: str
    item: list[OrderItemResponse]

class CheckoutResponse(BaseModel):
    message: str
    id_order: int
    total_price: int
    status: str

class CheckoutProduct(BaseModel):
    quantity: int = Field(gt=0)