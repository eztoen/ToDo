from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Tasks
from .schemas import TaskCreate

async def get_tasks(session: AsyncSession) -> list[Tasks]:
    stmt = select(Tasks).order_by(Tasks.date)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)

async def get_task_by_date(session: AsyncSession, date) -> Tasks | None:
    return await session.get(Tasks, date)

async def create_task(session: AsyncSession, new_task: TaskCreate):
    product = Tasks(**new_task.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

async def update_task_status(session: AsyncSession, task_id):
    ...
    
async def update_task_status(session: AsyncSession, task_id):
    ...
    
async def delete_task(session: AsyncSession, task_id):
    ...