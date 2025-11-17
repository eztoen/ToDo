from fastapi import Depends, HTTPException, status
from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from core.security import security, oauth2_scheme
from core.models import Users
from .schemas import UserRegister, UserLogin, TokenResponse

async def register_user(new_user: UserRegister, session: AsyncSession):
    stmt = select(Users).where(Users.email == new_user.email)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The email you have provided is already associated with an account'
        )
        
    user = Users(
        username = new_user.username,
        email = new_user.email,
        hashed_password = security.get_password_hash(new_user.password)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return TokenResponse(
        success=True,
        message='You have successfully registered',
        access_token=None,
        refresh_token=None,
        token_type=None,
    )


async def login_user(user_data: UserLogin, session: AsyncSession, redis: Redis):
    stmt = select(Users).where(Users.email == user_data.email)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not security.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials. Please try again'
        )
        
    access_token = security.create_access_token({'sub': str(user.id)})
    refresh_token = security.create_access_token({'sub': str(user.id)})
    
    await redis.set(
        f'refresh:{user.id}',
        refresh_token,
        ex=security.REFRESH_TOKEN_EXPIRE_DAYS * 86400
    )
    
    return TokenResponse(
        success=True,
        message='You have successfully logged into your account',
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer',
    )
    
