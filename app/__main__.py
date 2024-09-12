from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers.auth.auth_router import router as auth_router
from app.routers.tasks.tasks_router import router as tasks_router
from app.routers.auth.logout import router as logout_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(logout_router)



if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
