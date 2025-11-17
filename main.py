import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.models import Base, db_helper, redis_helper
from api.tasks.views import router as task_router
from api.auth.views import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    app.state.redis = await redis_helper.get_client()
    
    yield
    
    await redis_helper.close()
    await db_helper.async_engine.dispose()
        
app = FastAPI(lifespan=lifespan)

app.include_router(task_router)
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)