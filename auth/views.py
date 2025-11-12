from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import UserRegister, UserLogin, TokenResponse
from core.models import get_db

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model=TokenResponse)
async def register_user(new_user: UserRegister, session: AsyncSession = Depends(get_db)):
    return await crud.register_user(new_user=new_user, session=session)

@router.post('/login', response_model=TokenResponse)
async def login_user(user_data: UserLogin, session: AsyncSession = Depends(get_db)):
    return await crud.login_user(user_data=user_data, session=session)