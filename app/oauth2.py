from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import model
from . import schema
from . import database
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM=os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

def create_token(data: dict):
    data_copy = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expire})

    encoded = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)

    return encoded

def verify_token(token: str, exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("seller_id")

        if id is None:
            raise exception

        token_data = schema.TokenData(id=id)
    except JWTError:
        raise exception

    return token_data

def get_seller(token: str = Depends(oauth2), db: Session = Depends(database.get_db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                              detail=f"Could not validate", 
                              headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, exception)

    seller = db.query(model.Seller).filter(model.Seller.id == token.id).first()

    return seller
