from sqlalchemy import (
    Column, 
    String
)

from .base import Base

class Users(Base):
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)