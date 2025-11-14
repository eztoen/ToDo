from sqlalchemy import (
    Integer,
    Column,
    ForeignKey, 
    String, 
    Date, 
    Enum as SQLEnum
)

from enum import Enum

from .base import Base

class TaskStatus(str, Enum):
    CURRENT = 'current'
    EXPIRE = 'expire'
    TODAY = 'today'
    DONE = 'done'

class Tasks(Base):
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.CURRENT)
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)