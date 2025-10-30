from datetime import date
from sqlalchemy import delete, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Tasks
from .schemas import TaskCreate

async def get_tasks(session: AsyncSession) -> list[Tasks]:
    stmt = select(Tasks).order_by(Tasks.date)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)

async def get_task_by_date(session: AsyncSession, date: date) -> list[Tasks]:
    stmt = select(Tasks).where(Tasks.date == date)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)

async def create_task(session: AsyncSession, new_task: TaskCreate):
    task = Tasks(**new_task.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def update_task_status(session: AsyncSession, task_id):
    ...
    
async def update_task_status(session: AsyncSession, task_id):
    ...
    
async def delete_task(session: AsyncSession, task_id):
    stmt = delete(Tasks).where(Tasks.id == task_id)
    result: Result = await session.execute(stmt)
    await session.commit()
    return result.rowcount