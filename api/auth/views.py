from redis import Redis
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import UserRegister, UserLogin, TokenResponse

from core.models import get_db, rate_limiter, redis_helper
from core.security import security

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model=TokenResponse)
@rate_limiter(limit=10, period=300)
async def register_user(request: Request, new_user: UserRegister, session: AsyncSession = Depends(get_db)):
    return await crud.register_user(
        new_user=new_user, 
        session=session
    )

@router.post('/login', response_model=TokenResponse)
@rate_limiter(limit=10, period=600)
async def login_user(request: Request, user_data: UserLogin, redis: Redis = Depends(redis_helper.get_client), session: AsyncSession = Depends(get_db)):
    return await crud.login_user(
        user_data=user_data, 
        session=session, 
        redis=redis
    )

@router.post('/logout')
async def logout_user(user_id: int = Depends(security.get_user_id), redis: Redis = Depends(redis_helper.get_client), session: AsyncSession = Depends(get_db)):
    return await crud.logout_user(
        user_id=user_id,
        redis=redis,
        session=session
    )