from fastapi import HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from core.security import security
from core.models import Users
from .schemas import ChangePassword, ChangeUsername, ChangeEmail, SettingsResponse, DeleteAccount


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
    
async def change_password(user_id: int, session: AsyncSession, password = ChangePassword):
    select_stmt = select(Users).where(Users.id == user_id)
    result: Result = await session.execute(select_stmt)
    user = result.scalars().first()
    
    if not security.verify_password(password.actual_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid password'
    )
    
    update_stmt = (
        update(Users)
        .where(Users.id == user_id)
        .values(hashed_password=security.get_password_hash(password.new_password))
    )
    
    await session.execute(update_stmt)
    await session.commit()
    
    return SettingsResponse(
        success=True,
        message='You have successfully changed your password'
    )
    
async def delete_account(redis, user_id: int, session: AsyncSession, delete_user: DeleteAccount):
    if not delete_user.confirmation_message == 'DELETE MY ACCOUNT':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message='Invalid confirmation message'
        )
        
    delete_stmt = (
        delete(Users)
        .where(Users.id == user_id)
    )
    
    key = f'refresh:{user_id}'
    exists = await redis.exists(key)
    
    if exists:
        await redis.delete(key)
        
    await session.execute(delete_stmt)
    await session.commit()
    
    return SettingsResponse(
        success=True,
        message='You have delete your account'
    )