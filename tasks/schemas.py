from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class TaskStatus(str, Enum):
    current = 'current'
    expire = 'expire'
    today = 'today'
    done = 'done'
    
class TaskBase(BaseModel):
    title: str = Field(max_length=255)
    date: date
    status: TaskStatus 
    
class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    class Congif:
        orm_mode = True