from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import SessionLocal
from backend.models.user import User
from backend.schemas.user import UserCreate, UserOut
from backend.routes.auth_utils import hash_password, verify_password, create_access_token, decode_access_token

# No prefix here because it's added in main.py
router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)

    db_user = User(
        email=user.email,
        password=hashed,
        name=user.name,
        role=user.role,
        location=user.location
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Form login for Swagger UI 'Authorize' button (Handles /auth/login)"""
    return perform_login(form_data.username, form_data.password, db)


@router.post("/login-json")
def login_json(data: LoginRequest, db: Session = Depends(get_db)):
    """JSON login for frontend (Handles /auth/login-json)"""
    return perform_login(data.email, data.password, db)


def perform_login(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    }
