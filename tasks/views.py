from datetime import date
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import Task, TaskCreate

router = APIRouter(prefix='/tasks', tags=['Tasks'])

@router.get('/', response_model=list[Task])
async def get_tasks(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    tasks = await crud.get_tasks(session=session)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='You dont have any tasks yet'
)
    return tasks
        
@router.get('/{date}', response_model=list[Task])
async def get_tasks_by_date(date: date, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    tasks = await crud.get_task_by_date(session=session, date=date)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='You dont have any tasks for this day yet'
)
    return tasks

@router.post('/', response_model=Task)
async def create_task(new_task: TaskCreate, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await crud.create_task(session=session, new_task=new_task)

@router.delete('/')
async def delete_task(task_id: int, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await crud.delete_task(session=session, task_id=task_id)