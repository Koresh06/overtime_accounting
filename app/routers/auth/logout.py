from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from app.routers import templates



router = APIRouter()


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    msg = "Выход выполнен успешно"
    response = templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "msg": msg,
        },
    )
    response.delete_cookie(key="access_token")
    return response