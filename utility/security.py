from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, UTC
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError
from dotenv import load_dotenv

import os
import jwt
import app.database.setup_db as setup_db
import app.models.model as model

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/login"
)

def create_access_token(id_user: int) -> str:
    payload = {
        "id_user": id_user,
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token: str) -> dict:
    try:
        access = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]  
        )
        return access
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token invalid"
        )
    
def get_current_user(
        token: str = Depends(oauth2_schema),
        db: Session = Depends(setup_db.get_db)
) -> model.User:
    payload = verify_token(token)
    
    user = db.query(model.User).filter(
        model.User.id_user == payload["id_user"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user