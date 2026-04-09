from fastapi import FastAPI
from database import engine, Base

from routes import auth, listings

# Create tables in PostgreSQL
Base.metadata.create_all(bind=engine)
app = FastAPI(title="FarmConnect API", description="API for FarmConnect application", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(listings.router, prefix="/api", tags=["Listings"])


@app.get("/")
def root():
    return {"message": "FarmConnect API running 🚀"}
