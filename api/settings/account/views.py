from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import ChangeUsername, SettingsResponse

from core.models import get_db, rate_limiter
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