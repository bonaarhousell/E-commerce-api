from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.setup_db import get_db
from utility.security import get_current_user

import app.models.model as model
import app.schemas.schemas as schemas

router = APIRouter()

@router.post("/cart/product", status_code=201)
def add_product_to_cart(
    product: schemas.AddProductToCart,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    get_product = db.query(model.Product).filter(
        model.Product.id_product == product.id_product
    ).first()

    if not get_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    cart = db.query(model.Cart).filter(
        model.Cart.id_user == current_user.id_user
    ).first()

    if not cart:
        cart = model.Cart(
            id_user = current_user.id_user,
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)
    existing_item = db.query(model.CartItem).filter(
        model.CartItem.id_cart == cart.id_cart,
        model.CartItem.id_product == product.id_product
    ).first()

    if existing_item:
         existing_item.quantity += product.quantity
    else:
        new_item = model.CartItem(
            id_cart = cart.id_cart,
            id_product = get_product.id_product,
            quantity = product.quantity
        )
        db.add(new_item)
    db.commit()

    return {
        "message": "product successfully add to cart",
        "id_product": new_item.id_product
    }

@router.get("/cart", response_model=schemas.CartResponse)
def get_info_cart(
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = db.query(model.Cart).filter(
        model.Cart.id_user == current_user.id_user
    ).first()

    if not cart:
        return {
        "items": [],
        "total_cart_price": 0
    }
    total_cart_price = 0
    items = []
    for item in cart.cart_items:
        subtotal = (item.quantity * item.products.price_product)
        items.append(
            {
                "id_product": item.id_product,
                "name_product": item.products.name_product,
                "quantity": item.quantity,
                "subtotal": subtotal
            }
        )
        total_cart_price += subtotal

    return {
        "items": items,
        "total_cart_price": total_cart_price,
    }

@router.delete("/cart/product/{id_product}")
def remove_product_from_cart(
    id_product: int,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = db.query(model.Cart).filter(
        model.Cart.id_user == current_user.id_user
    ).first()
    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )
    
    cart_item = db.query(model.CartItem).filter(
        model.CartItem.id_cart == cart.id_cart,
        model.CartItem.id_product == id_product
    ).first()
    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )
    db.delete(cart_item)
    db.commit()
    return {
        "message": "product removed from cart",
        "id_product": id_product
    }

    
@router.put("/cart/product/{id_product}")
def update_product_in_cart(
    id_product: int,
    product: schemas.UpdateCartItem,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = db.query(model.Cart).filter(
        model.Cart.id_user == current_user.id_user
    ).first()
    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )
    
    cart_item = db.query(model.CartItem).filter(
        model.CartItem.id_cart == cart.id_cart,
        model.CartItem.id_product == id_product
    ).first()
    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )
    if product.new_quantity > cart_item.products.stock:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )
    cart_item.quantity = product.new_quantity
    db.commit()
    return {
        "message": "Cart updated",
        "id_product": id_product,
        "quantity": cart_item.quantity
}