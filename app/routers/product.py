from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.setup_db import get_db
from utility.security import get_current_user
from app.logger import logger

import app.models.model as model
import app.schemas.schemas as schemas

router = APIRouter()

@router.post("/product", status_code=201)
def create_product(
    product: schemas.ProductCreate,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(model.User).filter(
        model.User.id_user == current_user.id_user
    ).first()

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can create product"
        )
    
    new_product = model.Product(
        name_product = product.name_product,
        price_product = product.price_product,
        stock = product.stock,
        category_product = product.category_product,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    logger.info(
        "Admin id %s Create new product id (%s)",
        current_user.id_user,
        create_product.id_product
    )
    return {
        "message": "Product created",
        "id_product": new_product.id_product
    }

@router.get("/product", response_model=list[schemas.ProductResponse])
def get_all_product(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    category: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(model.Product)
    if category:
        query = query.filter(
            model.Product.category_product == category
        )

    if search:
        query = query.filter(
            model.Product.name_product.ilike(f"%{search}%")
        )
    skip = (page - 1) * limit 
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/product/{id_product}", response_model=schemas.ProductDetailResponse)
def get_detail_product(
    id_product: int,
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

    sold = db.query(
        func.coalesce(func.sum(model.OrderItem.quantity), 0)
        ).filter(
            model.OrderItem.id_product == id_product
        ).scalar()

    return {
        "id_product": id_product,
        "name_product": product.name_product,
        "price_product": product.price_product,
        "category_product": product.category_product,
        "stock": product.stock,
        "product_sold": sold
    }


@router.put("/product/{id_product}")
def update_product(
    id_product: int,
    product: schemas.ProductUpdate,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can update the product"
        )
    
    update_product = db.query(model.Product).filter(
        model.Product.id_product == id_product
    ).first()

    if not update_product:
        raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

    update_product.name_product = product.name_product
    update_product.price_product = product.price_product
    update_product.category_product = product.category_product
    update_product.stock = product.stock

    db.commit()
    db.refresh(update_product)
    logger.info(
        "Admin id %s Update product id %s",
        current_user.id_user,
        update_product.id_product
    )
    return {
        "message" : "product Succesfully updated",
        "new_product_name": update_product.name_product,
        "id_product": update_product.id_product
    }

@router.put("/product/stock/{id_product}")
def update_product_stock(
    id_product: int,
    product: schemas.ProductUpdateStock,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can update the product"
        )
    
    update_product = db.query(model.Product).filter(
        model.Product.id_product == id_product
    ).first()

    if not update_product:
        raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

    update_product.stock = product.stock

    db.commit()
    db.refresh(update_product)
    logger.info(
        "Admin id %s Updated stock product id %s",
        current_user.id_user,
        update_product.id_product
    )
    return {
        "message" : "Product Succesfully updated",
        "new_product_stock": update_product.stock,
        "id_product": update_product.id_product
    }

@router.delete("/product/{id_product}")
def remove_product(
    id_product: int,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can remove the product"
        )
    
    delete_product = db.query(model.Product).filter(
        model.Product.id_product == id_product
    ).first()

    if not delete_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    db.delete(delete_product)
    db.commit()
    logger.info(
        "Admin id %s Remove product id %s",
        current_user.id_user,
        delete_product.id_product
    )
    return {
        "message": "Product Successfully removed",
        "id_product": id_product
    }
