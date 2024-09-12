from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, Request, Response, status, APIRouter, Form
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.db_halper import db_helper
from app.routers import templates
from app.routers.auth.auth_schemas import LoginForm, RegisterUserSchema, Token
from app.core.service.auth_service import AuthService
from app.core.models.users import Users
from app.routers.auth.dependence import authenticate_user
from app.routers.auth.security import create_access_token, get_password_hash
from app.routers.auth.dependence import get_current_user



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        401: {"user": "Not authorized"},
    },
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user: Users = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        session=session,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(
        data={
            "sub": user.username,
            "id": user.id,
        },
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
    session: Annotated[Session, Depends(db_helper.get_db)],
):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()

        validate_user_cookie = await login_for_access_token(
            response=Response(),
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

        response = RedirectResponse(url="/tasks/", status_code=status.HTTP_302_FOUND)

        response.set_cookie(
            key="access_token",
            value=validate_user_cookie.access_token,
            httponly=True,
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
    user_register: RegisterUserSchema = Depends(RegisterUserSchema.as_form),
):
    try:
        validation1 = AuthService(session).validate_username(user_register. username)
        validation2 = AuthService(session).validate_email(user_register.email)

        if user_register.password != user_register.password2 or validation1 is not None or validation2 is not None:
            msg = "Неверный запрос на регистрацию"
            return templates.TemplateResponse(
                "register.html",
                {
                    "request": request,
                    "msg": msg,
                },
            )

        user_model = Users(
            email=user_register.email,
            username=user_register.username,
            first_name=user_register.first_name,
            last_name=user_register.last_name,
            hashed_password=get_password_hash(user_register.password),
        )

        AuthService(session).create_user_db(user_model)

    except HTTPException as e:
        msg = "Неизвестная ошибка"
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "msg": msg,
            },
        )

    msg = "Пользователь успешно создан"
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "msg": msg,
        },
    )


@router.get("/me")
async def get_me(
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
    user: Users = Depends(get_current_user),
):
    return user
