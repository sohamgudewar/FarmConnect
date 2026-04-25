from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.database import engine, Base
from backend.routes import auth, listings, prices
from backend.models import market_price  # Ensure model is loaded for migrations
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables in PostgreSQL
    try:
        logger.info("Connecting to the database and creating tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        # In a real app, you might want to exit here if the DB is critical
    
    yield
    # Shutdown logic (if any) can go here
    logger.info("Shutting down application...")

app = FastAPI(
    title="FarmConnect API", 
    description="API for FarmConnect application", 
    version="1.0.0",
    lifespan=lifespan
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(listings.router, prefix="/api", tags=["Listings"])
app.include_router(prices.router, prefix="/api", tags=["Market Prices"])

@app.get("/")
def root():
    return {"message": "FarmConnect API running 🚀"}
