from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, Request, Response, status, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.db_halper import db_helper
from app.utils.assistants_auth import (
    get_password_hash,
    verify_password,
    authenticate_user,
    create_access_token,
)
from app.routers.schemas.auth_schemas import LoginForm, Token
from app.core.service.auth_service import AuthService
from app.core.models.users import Users


templates = Jinja2Templates(directory="app/templates")


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        401: {"user": "Not authorized"},
    },
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        session=session,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        role=user.role,
        expires_delta=timedelta(minutes=60),
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
    )

    return Token(access_token=token, token_type="bearer")


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(
    request: Request,
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/tasks/", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(
            response=response,
            form_data=form,
            session=session,
        )

        if not validate_user_cookie:
            msg = "Неверное имя пользователя или пароль"
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "msg": msg,
                },
            )
        return response
    except HTTPException as e:
        msg = "Неизвестная ошибка"
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "msg": msg,
            },
        )


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
    email: str = Form(...),
    username: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
):

    validation1 = AuthService(session).validate_username(username)
    validation2 = AuthService(session).validate_email(email)

    if password != password2 or validation1 is not None or validation2 is not None:
        msg = "Неверный запрос на регистрацию"
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "msg": msg,
            },
        )

    user_model = Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = first_name
    user_model.last_name = last_name

    hash_password = get_password_hash(password)
    user_model.hashed_password = hash_password
    user_model.is_active = True

    session.add(user_model)
    session.commit()
    session.refresh(user_model)

    msg = "Пользователь успешно создан"
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "msg": msg,
        },
    )


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