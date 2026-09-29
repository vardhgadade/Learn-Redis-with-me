from fastapi import FastAPI
from app.apis.users import router as users_router
import uvicorn 
from app.database.database import Settings
from contextlib import asynccontextmanager
import redis.asyncio as aioredis
import redis
from app.routers.redis.redis import router as redis_router
from app.limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


redis_client:aioredis.Redis | None=None 



@asynccontextmanager 
async def lifespan(app:FastAPI):

    #Initilize redis connection 
    client=redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )
    client.ping()
    app.state.redis=client
 
    print("Redis Is Connected succefully")
    
    try:
        yield
    finally:
        await redis.close()



app=FastAPI(title="Backend for Redis",lifespan=lifespan)
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
app.include_router(users_router)
app.include_router(redis_router)

@app.get("/")
def root()->dict[str,str]:
    return {"status":"OK"}



if __name__=="__main__":
   uvicorn.run(
    "app.main:app",
    host=Settings.APP_HOST,
    port=Settings.APP_PORT,
    reload=True
   )