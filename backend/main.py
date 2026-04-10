from fastapi import FastAPI
from backend.database import engine, Base
from backend.routes import auth, listings

# Create tables in PostgreSQL (if not exists)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FarmConnect API", description="API for FarmConnect application", version="1.0.0")

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(listings.router, prefix="/api", tags=["Listings"])


@app.get("/")
def root():
    return {"message": "FarmConnect API running 🚀"}
