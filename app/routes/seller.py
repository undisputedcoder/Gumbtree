"""Seller Router

Holds all the routes for a seller
"""

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import utils
from .. import model, oauth2, schema
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/seller",
    tags=['Sellers']
)

# Create an account for a seller
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.SellerResponse)
def create_seller(body: schema.Seller, db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(body.password)
    body.password = hashed_pwd

    seller = model.Seller(**body.dict())
    db.add(seller)
    db.commit()
    db.refresh(seller)

    return seller

# Retrieve a seller
@router.get("/{id}", response_model=schema.SellerResponse)
def get_seller(id: int, db: Session = Depends(get_db)):
    seller = db.query(model.Seller).filter(model.Seller.id == id).first()

    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"seller id {id} not found")
    return seller


# Login in with email and password
@router.post("/login", response_model=schema.Token)
def create_seller(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    seller = db.query(model.Seller).filter(
        model.Seller.email == body.username).first()

    if not seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="invalid credentials")

    if not utils.verify(body.password, seller.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="invalid credentials")

    token = oauth2.create_token(data = {"seller_id": seller.id})

    return {"token": token, "token_type" : "bearer"}