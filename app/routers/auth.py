from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utility.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.logger import logger

import bcrypt
import app.database.setup_db as setup_db
import app.models.model as model
import app.schemas.schemas as schemas

router = APIRouter()

@router.post("/register", status_code=201)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(setup_db.get_db)
):
    existing_user = db.query(model.User).filter(
        model.User.username == user.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=401,
            detail="Username already use"
        )
    password_hash = bcrypt.hashpw(user.password.encode(),bcrypt.gensalt()).decode()
    new_user = model.User(
            username = user.username,
            password_hash = password_hash,
            email = user.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(
        "New user create account with id %s",
        new_user.id_user
    )
    return {
        "message": "Register successfully",
        "id_user": new_user.id_user
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(setup_db.get_db)
):
    user = db.query(model.User).filter(
        model.User.username == form_data.username
    ).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="invalid Username"
        )
    if not bcrypt.checkpw(form_data.password.encode(), user.password_hash.encode()):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )
    token = create_access_token(user.id_user)
    logger.info(
        "User id %s login",
        user.id_user
    )
    return {
        "access_token": token,
        "token_type": "Bearer",
        "Expired": 3600
    }

