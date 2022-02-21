"""Listing Router

Holds all the routes for a Listing
"""
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter

from .. import schema

from .. import model, oauth2
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/listings",
    tags=['Listings']
)

# 1a. Retrieve all the listings
@router.get("/", response_model=List[schema.ListingOut])
def get_listings(db: Session = Depends(get_db)): 
    listings = db.query(model.Listing).all()
    return listings

# 1b. Retrieve a single listing(must provide the listing id)
@router.get("/{id}")
def get_listing(id: int, db: Session = Depends(get_db)):
    listing = db.query(model.Listing).filter(model.Listing.id == id).first()

    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"listing id {id} not found")
    return listing


# Create a listing
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_listings(body: schema.ListingCreate, db: Session = Depends(get_db), uid: int = Depends(oauth2.get_seller)):
    listing = model.Listing(seller_id=uid.id, **body.dict())
    db.add(listing)
    db.commit()
    db.refresh(listing)

    return listing


# Update a listing(must provide the listing id)
@router.put("/{id}")
def update_listing(id: int, body: schema.Listing, db: Session = Depends(get_db), uid: int = Depends(oauth2.get_seller)):
    listing = db.query(model.Listing).filter(model.Listing.id == id)

    if listing.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"listing {id} does not exist")

    if listing.first().seller_id != uid.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform request action")

    listing.update(body.dict(), synchronize_session=False)
    db.commit()
    
    return listing.first()


# Delete a listing(must provide the listing id)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(id: int, db: Session = Depends(get_db), uid: int = Depends(oauth2.get_seller)):
    listing = db.query(model.Listing).filter(model.Listing.id == id)

    if listing.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"listing {id} does not exist")

    if listing.first().seller_id != uid.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform request action")

    listing.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)