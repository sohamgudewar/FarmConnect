from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    location: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    location: str

    class Config:
        from_attributes = True
