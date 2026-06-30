from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utility.security import get_current_user

import app.schemas.schemas as schemas
import app.database.setup_db as setup_db
import app.models.model as model

router = APIRouter()

@router.get("/order", response_model=list[schemas.OrderResponse])
def get_list_order(
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):
    order = db.query(model.Order).filter(
        model.Order.id_user == current_user.id_user
    ).all()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order Empty"
        )
    return order

@router.get("/order/{id_order}", response_model=schemas.OrderItemDetailResponse)
def get_list_order_filter_by_id(
    id_order: int,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):
    order = db.query(model.Order).filter(
        model.Order.id_user == current_user.id_user,
        model.Order.id_order == id_order
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    
    order_item = []
    for item in order.order_items:
        order_item.append(
            {
                "id_product": item.id_product,
                "name_product":item.products.name_product,
                "quantity": item.quantity,
                "unit_price": item.products.price_product,
                "subtotal": item.quantity * item.products.price_product
            }
        )
    return {
        "id_order": order.id_order,
        "total_price": order.total_price,
        "status": order.status,
        "item": order_item
    }        