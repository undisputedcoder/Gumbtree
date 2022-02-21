from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text

class Listing(Base):
    __tablename__ = "listing"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    listed = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    condition = Column(String, nullable=False) # add constraints (New, Used)
    seller_id = Column(Integer, ForeignKey("seller.id", ondelete="CASCADE"), nullable=False)
    
    seller = relationship("Seller")

class Seller(Base):
    __tablename__ = "seller"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    joined = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    password = Column(String, nullable=False)