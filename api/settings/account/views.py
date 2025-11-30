from redis import Redis
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import ChangePassword, ChangeUsername, SettingsResponse, ChangeEmail, DeleteAccount

from core.models import get_db, rate_limiter, redis_helper
from core.security import security

router = APIRouter(prefix='/account', tags=['settings'])

@router.patch('/change-username', response_model=SettingsResponse)
@rate_limiter(limit=1, period=86400)
async def change_username(
    request: Request,
    new_username: ChangeUsername, 
    user_id: int = Depends(security.get_user_id), 
    session: AsyncSession = Depends(get_db)
    ):
    return await crud.change_username(
        user_id=user_id,
        session=session,
        new_username=new_username
    ) 

@router.patch('/change-email', response_model=SettingsResponse)
@rate_limiter(limit=1, period=86400)
async def change_email(
    request: Request,
    new_email: ChangeEmail, 
    user_id: int = Depends(security.get_user_id), 
    session: AsyncSession = Depends(get_db)
):
    return await crud.change_email(
        user_id=user_id,
        session=session,
        new_email=new_email
    )
    
@router.patch('/change-password', response_model=SettingsResponse)
@rate_limiter(limit=1, period=86400)
async def change_password(
    request: Request,
    password: ChangePassword,
    user_id: int = Depends(security.get_user_id), 
    session: AsyncSession = Depends(get_db),
):
    return await crud.change_password(
        user_id=user_id,
        session=session,
        password=password
    )
    
@router.delete('/delete-account', response_model=SettingsResponse)
async def delete_account(
    delete_user: DeleteAccount,
    redis: Redis = Depends(redis_helper.get_client),
    user_id: int = Depends(security.get_user_id),
    session: AsyncSession = Depends(get_db)
):
    return await crud.delete_account(
        redis=redis,
        user_id=user_id,
        session=session,
        delete_user=delete_user
    )