from fastapi import FastAPI
from app.apis.users import router as users_router
import uvicorn 
from app.database.database import settings
app=FastAPI(title="Backend for Redis")

app.include_router(users_router)

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