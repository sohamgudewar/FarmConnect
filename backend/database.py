import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Use environment variables for configuration - in production, always set these!
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/FarmConnect"
)

# engine = create_engine(DATABASE_URL)
# For SQLite, use: engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
