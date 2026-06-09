#import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://inventory_user:password123@localhost:5432/sistem_inventory"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
