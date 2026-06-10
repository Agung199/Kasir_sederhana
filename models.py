
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey
)

from sqlalchemy.orm import relationship
from database import Base




# Models item
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    stock = Column(Integer, default=0)
    price = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "stock": self.stock,
            "price": self.price,
        }


# Models User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True)

    email = Column(String(255), unique=True)

    password_hash = Column(String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Models STock Movement
class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True)

    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    movement_type = Column(String)

    quantity = Column(Integer)

    notes = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("Item")
