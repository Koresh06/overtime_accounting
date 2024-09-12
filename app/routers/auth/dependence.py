from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, status

from app.core.db_halper import db_helper
from app.core.models.users import Users
from app.core.service.auth_service import AuthService
from app.config import settings
from app.routers.auth.logout import logout
from .security import bcrypt_context, verify_password


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")
ookie_scheme = APIKeyCookie(name="session")


def authenticate_user(
    username: str,
    password: str,
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
):
    user: Users = AuthService(session).authenticate_user_db(username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
    request: Request,
    token: str = Depends(oauth2_bearer),
    # cookie: str = Depends(ookie_scheme),
):
    сredentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    ),
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(
            token,
            key=settings.auth.SECRET_KEY,
            algorithms=[settings.auth.ALGORITHM],
        )

        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            logout(request)

    except JWTError:
        raise сredentials_exception
    user = AuthService(session).get_user_by_id(user_id)
    if not user:
        raise сredentials_exception
    return user
