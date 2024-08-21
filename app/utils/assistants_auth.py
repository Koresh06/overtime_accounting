from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, status
from jose import ExpiredSignatureError, jwt, JWTError
from passlib.context import CryptContext

from app.core.db_halper import db_helper
from app.core.service.auth_service import AuthService
from app.config import settings



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(
    username: str,
    password: str,
    session: Annotated[
        Session,
        Depends(db_helper.get_db),
    ],
):
    user = AuthService(session).authenticate_user(username)

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str,
    user_id: int,
    role: str,
    expires_delta: timedelta = None,
):
    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(
        encode,
        key=settings.auth.secret_key,
        algorithm=settings.auth.algorithm,
    )


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(token, key=settings.auth.secret_key, algorithms=[settings.auth.algorithm])

        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        
        if username is None or user_id is None:
            logout(request)

        return {
            "username": username,
            "id": user_id,
            "role": user_role,
        }
    except ExpiredSignatureError:
        return None
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Found",
        )
