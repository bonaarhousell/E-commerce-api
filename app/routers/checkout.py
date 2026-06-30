from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.setup_db import get_db
from utility.security import get_current_user
from app.logger import logger

import app.models.model as model
import app.schemas.schemas as schemas

router = APIRouter()



@router.post("/checkout/{id_product}", response_model=schemas.CheckoutResponse)
def checkout_product(
    id_product : int,
    checkout: schemas.CheckoutProduct,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(model.Product).filter(
        model.Product.id_product == id_product
    ).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    if product.stock < checkout.quantity:
        raise HTTPException(
            status_code=400,
            detail="Product not have enough stock"
        )

    new_order = model.Order(
        id_user = current_user.id_user,
        total_price = checkout.quantity * product.price_product,
        status = "paid"
    )
    db.add(new_order)
    db.flush()

    order_item = model.OrderItem(
        id_order = new_order.id_order,
        id_product = product.id_product,
        quantity =  checkout.quantity,
        unit_price = product.price_product,
        subtotal = checkout.quantity * product.price_product
    ) 

    db.add(order_item)

    product.stock -= checkout.quantity

    db.commit()
    db.refresh(order_item)
    logger.info(
        "User id %s Checkout product id %s",
        current_user.id_user,
        order_item.id_product
    )
    return {
        "message": "Checkout Successfully",
        "id_order": order_item.id_order,
        "total_price": new_order.total_price,
        "status": new_order.status,
    }

@router.post("/checkout", response_model=schemas.CheckoutResponse)
def checkout_product_from_cart(
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        cart = db.query(model.Cart).filter(
            model.Cart.id_user == current_user.id_user
        ).first()

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Cart not found"
            )
        
        cart_item = cart.cart_items
        if not cart_item:
            raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )
        for item in cart_item:
            if item.products.stock < item.quantity:
                raise HTTPException(
                status_code=400,
                detail="Stock is insufficient"
            ) 
        total_price = 0
        for item in cart_item:
            total_price += (item.quantity * item.products.price_product)

        order = model.Order(
                id_user = current_user.id_user,
                total_price = total_price,
                status = "paid"
            )
        db.add(order)
        db.flush()

        for item in cart_item:
            order_item = model.OrderItem(
                id_order = order.id_order,
                id_product = item.products.id_product,
                quantity = item.quantity,
                unit_price = item.products.price_product,
                subtotal = item.quantity * item.products.price_product
            )
            item.products.stock -= item.quantity
            db.add(order_item)
            db.delete(item)
        
        db.commit()
        logger.info(
            "user id %s created order id %s",
            current_user.id_user,
            order.id_order
        )
        return {
            "message": "Checkout Successfully",
            "id_order" : order.id_order,
            "total_price": order.total_price,
            "status": order.status
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        logger.exception("unexpected error while user id %s checkout product",
                         current_user.id_user,
                         )
        raise