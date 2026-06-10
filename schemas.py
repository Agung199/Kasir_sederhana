from pydantic import BaseModel


# Ragister
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


# Login
class UserLogin(BaseModel):
    username: str
    password: str


# Item
class ItemCreate(BaseModel):
    name: str
    stock: int
    price: float

class ItemUpdate(BaseModel):
    name: str | None = None
    stock: int | None = None
    price: float | None = None


# Stock
class StockRequest(BaseModel):
    item_id: int
    quantity: int
    notes: str | None = ""
