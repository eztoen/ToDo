from datetime import date
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import Task, TaskCreate

router = APIRouter(prefix='/tasks', tags=['Tasks'])

@router.get('/', response_model=list[Task])
async def get_tasks(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await crud.get_tasks(session=session)
        
@router.get('/{date}', response_model=list[Task])
async def get_tasks_by_date(date: date, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await crud.get_task_by_date(session=session, date=date)

@router.post('/', response_model=Task)
async def create_task(new_task: TaskCreate, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await crud.create_task(session=session, new_task=new_task)

@router.patch('/')
async def update_date(task_id: int, task_date: date, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await crud.update_task_date(session=session, task_id=task_id, new_task_date=task_date)

@router.delete('/')
async def delete_task(task_id: int, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await crud.delete_task(session=session, task_id=task_id)