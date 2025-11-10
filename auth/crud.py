from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from core.security import security
from core.models import Users
from .schemas import UserCreate

async def register(new_user: UserCreate, session: AsyncSession):
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
    
    token = security.create_access_token({'sub': str(user.id)})
    return {'access_token': token, 'token_type': 'bearer'}