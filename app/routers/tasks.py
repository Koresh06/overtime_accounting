from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.db_halper import db_helper
from app.utils.assistants_auth import get_current_user
from app.core.service.tasks_service import TasksService
from app.core.models.tasks import Tasks
from app.routers.schemas.tasks_schemas import TaskCreateSchema


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={
        404: {"description": "Not found"},
    },
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(
    request: Request,
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND)

    tasks = TasksService(session).get_all_tasks(user.get("id"))
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "tasks": tasks,
            "user": user,
        },
    )


@router.get("/create-task", response_class=HTMLResponse)
async def create_task(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        "create-task.html",
        {
            "request": request,
            "user": user,
        },
    )


@router.post("/create-task", response_class=HTMLResponse)
async def create_task(
    request: Request,
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
    task_data: TaskCreateSchema = Depends(TaskCreateSchema.as_form)
):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND)


    TasksService(session).create_task(task=task_data, user_id=user.get("id"))

    return RedirectResponse(url="/tasks/", status_code=status.HTTP_302_FOUND)
