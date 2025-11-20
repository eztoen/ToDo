from fastapi import Depends, HTTPException, status
from redis import Redis
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from core.security import security, oauth2_scheme
from core.models import Users
from .schemas import ChangeUsername, ChangeEmail, SettingsResponse


async def change_username(user_id: int, session: AsyncSession, new_username: ChangeUsername):
    select_stmt = select(Users).where(Users.username == new_username.username)
    result: Result = await session.execute(select_stmt)
    
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already taken'
    )
    
    update_stmt = (
        update(Users)
        .where(Users.id == user_id)
        .values(username=new_username.username)
    )
    
    await session.execute(update_stmt)
    await session.commit()
    
    return SettingsResponse(
        success=True,
        message='You have successfully changed your username'
    )
    
async def change_email(user_id: int, session: AsyncSession, new_email: ChangeEmail):
    select_stmt = select(Users).where(Users.email == new_email.email)
    result: Result = await session.execute(select_stmt)
    
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already taken'
    )
    
    update_stmt = (
        update(Users)
        .where(Users.id == user_id)
        .values(email=new_email.email)
    )
    
    await session.execute(update_stmt)
    await session.commit()
    
    return SettingsResponse(
        success=True,
        message='You have successfully changed your email'
    )