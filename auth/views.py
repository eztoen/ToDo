from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import UserRead, UserCreate, Token
from core.models import get_db

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model=Token)
async def register(new_user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await crud.register(new_user=new_user, session=session)