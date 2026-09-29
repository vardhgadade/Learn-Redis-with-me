from fastapi import APIRouter,HTTPException,Request
from app.schemas.user import  RedisValue as StringInput, ListValue as ListInput
from app.limiter import limiter


router=APIRouter(
    prefix="/redis",
    tags=["redis"]
)

@router.get("/string/{key}")
async def get_value(key:str,request:Request):
    redis_client=request.app.state.redis
    value=await client.get(key)

    if value is None:
        raise HTTPException(
            status_code=404,
            detail=f"Key '{key}' not found in Redis"
        )

    return{
        "key":key,
        "value":value
    }


@router.post("string/user/{user_id}")
def set_user_value(\
      user_id:str,
      payload:StringInput,
      request:Request
    ):
    
    client=request.app.state.redis
    redis_key=f"user:{user_id}"

    client.set(redis_key,payload.value)
    
    #Here you can add ex it is expire time for that data in redis
    # client.set(redis_key,payload.value,ex=30)

    return {"key":redis_key,"value":payload.value}


@router.put("string/user/{user_id}")
def update_user_value(
        user_id:str,
        payload:StringInput,
        request:Request
    ):

    client=request.app.state.redis
    redis_key=f"user:{user_id}"

    if not client.exists(redis_key):
        raise HTTPException(
            status_code=404,
            detail=f"user key '{redis_key}' not found in Redis"
        )
    
    client.set(redis_key,payload.value)
    return {"key":redis_key,"value":payload.value}

#Create a List in Redis using Code
@router.post("/list/{key}")
def creare_list_item(key:str,payload:ListInput,request:Request):
    try:
        client=request.app.state.redis
        if not client:
            raise HTTPException(
                status_code=503,
                detail="Cleint not exists"
            )
        
        # length=cleint.rpush(key,payload.value)
        length = client.rpush(key, payload.value)

        return{
            "key":key,
            "value":payload.value,
            "length":length,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Coulf not add value to redis list:{exc}"
        ) from exc

@router.get("/list/{key}")
@limiter.limit("5/minute")
def get_list(key:str,request:Request):
    Cleint=request.app.state.redis
    
    if not Cleint:
        raise HTTPException(
            status_code=404,
            detail=f"List '{key}' not found"
        )
    return {
        "key":key,
        "values":Cleint.lrange(key,0,-1)
    }

    