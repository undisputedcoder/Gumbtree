from fastapi import FastAPI
from . import model
from .database import engine
from .routes import listing, seller

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(listing.router)
app.include_router(seller.router)

@app.get("/")
def root():
    return {"message": "Hello World"}