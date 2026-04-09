from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# change username, password, db name
DATABASE_URL = "postgresql://postgres:password@localhost:5432/FarmConnect"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
