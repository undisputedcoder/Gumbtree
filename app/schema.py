from datetime import datetime
from email.policy import strict
from pydantic import BaseModel, EmailStr
from typing import Optional

from .database import Base 

class Seller(BaseModel):
    name: str
    email: EmailStr
    rating: int
    location: str
    password: str

class SellerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    rating: int
    location: str
    joined: datetime

    class Config:
        orm_mode = True
        
class Listing(BaseModel):
    name: str
    price: int
    condition: str

class ListingCreate(Listing):
    pass

class ListingOut(BaseModel):
    id: int
    name: str
    price: int
    condition: str
    listed: datetime
    seller: SellerResponse

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None