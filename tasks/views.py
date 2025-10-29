from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import Task

router = APIRouter(prefix='/tasks', tags=['Tasks'])

@router.get('/', response_model=list[Task])
async def get_tasks(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await crud.get_tasks(session=session)