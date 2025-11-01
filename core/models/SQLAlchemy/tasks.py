from sqlalchemy import (
    Column, 
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