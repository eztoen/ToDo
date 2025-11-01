from datetime import date
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import TaskRead, TaskCreate, TaskStatus
from core.models import rate_limiter, get_db

router = APIRouter(prefix='/tasks', tags=['Tasks'])

@router.get('/', response_model=list[TaskRead])
@rate_limiter(limit=35, period=300)
async def get_tasks(request: Request, session: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(session=session)
        
@router.get('/{date}', response_model=list[TaskRead])
@rate_limiter(limit=25, period=300)
async def get_tasks_by_date(request: Request, date: date, session: AsyncSession = Depends(get_db)):
    return await crud.get_task_by_date(session=session, date=date)

@router.post('/', response_model=TaskRead)
@rate_limiter(limit=35, period=300)
async def create_task(request: Request, new_task: TaskCreate, session: AsyncSession = Depends(get_db)):
    return await crud.create_task(session=session, new_task=new_task)

@router.patch('/status/{task_id}')
@rate_limiter(limit=50, period=600)
async def update_status(request: Request, task_id: int, task_status: TaskStatus, session: AsyncSession = Depends(get_db)):
    return await crud.update_task_status(session=session, task_id=task_id, new_status=task_status)

@router.patch('/deadline/{task_id}')
@rate_limiter(limit=50, period=600)
async def update_date(request: Request, task_id: int, task_date: date, session: AsyncSession = Depends(get_db)):
    return await crud.update_task_date(session=session, task_id=task_id, new_task_date=task_date)

@router.delete('/')
@rate_limiter(limit=20, period=300)
async def delete_task(request: Request, task_id: int, session: AsyncSession = Depends(get_db)):
    return await crud.delete_task(session=session, task_id=task_id)