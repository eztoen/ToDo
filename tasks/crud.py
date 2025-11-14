import json
from fastapi import HTTPException, status
from datetime import date
from redis import Redis
from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import security, oauth2_scheme

from core.models import Tasks, redis_helper, clear_task_cache
from .schemas import TaskCreate, TaskStatus, TaskRead

async def get_tasks(user_id: int, session: AsyncSession) -> list[Tasks]:
    stmt = select(Tasks).order_by(Tasks.date).where(Tasks.user_id == user_id)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='You dont have any tasks yet'
    )
    
    return list(tasks)

async def get_task_by_date(user_id: int, session: AsyncSession, date: date) -> list[Tasks]:
    redis: Redis = await redis_helper.get_client()
    cache_key = f'tasks:{user_id}:{date.isoformat()}'
    
    cached = await redis.get(cache_key)
    
    if cached:
        return [TaskRead(**task_data) for task_data in json.loads(cached)]
    
    stmt = select(Tasks).where(Tasks.user_id == user_id, Tasks.date == date)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='You dont have any tasks for this day yet'
    )
    
    task_read_models = [TaskRead.model_validate(t).model_dump(mode='json') for t in tasks]
    
    await redis.set(
        cache_key, 
        json.dumps(task_read_models), 
        ex=300
    )
    
    return [TaskRead.model_validate(t) for t in tasks]

async def create_task(user_id, session: AsyncSession, new_task: TaskCreate):
    task = Tasks(**new_task.model_dump(), user_id=user_id)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    clear_task_cache(new_task.date)
    
    return task

async def update_task_status(session: AsyncSession, user_id: int, task_id: int, new_status: TaskStatus):
    select_stmt = select(Tasks).where(Tasks.user_id == user_id, Tasks.id == task_id)
    result: Result = await session.execute(select_stmt)
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
    )
    
    task_date = task.date
    
    update_stmt = (
        update(Tasks)
        .where(Tasks.id == task_id)
        .values(status=new_status)
    )
    
    await session.execute(update_stmt)
    await session.commit()
    
    await clear_task_cache(task_date)
    
    return {'success': True, 'message': 'Status changed'}
    
async def update_task_date(session: AsyncSession, user_id: int, task_id: int, new_task_date: date):
    select_stmt = select(Tasks).where(Tasks.user_id == user_id, Tasks.id == task_id)
    result: Result = await session.execute(select_stmt)
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
    )
    
    old_date = task.date
    
    update_stmt = (
        update(Tasks)
        .where(Tasks.id == task_id)
        .values(date=new_task_date)
    )
    
    await session.execute(update_stmt)
    await session.commit()
    
    await clear_task_cache(old_date)
    await clear_task_cache(new_task_date)
    
    return {'success': True, 'message': 'Date changed'}
    
async def delete_task(session: AsyncSession, user_id: int, task_id: int):
    stmt = delete(Tasks).where(Tasks.user_id == user_id, Tasks.id == task_id)
    result: Result = await session.execute(stmt)
    await session.commit()
    return result.rowcount