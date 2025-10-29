from sqlalchemy import Column, String, Boolean, Date, Enum

import enum

from .base import Base

class TaskStatus(enum.Enum):
    CURRENT = 'current'
    EXPIRED = 'expire'
    TODAY = 'today'
    DONE = 'done'

class Tasks(Base):
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(TaskStatus))