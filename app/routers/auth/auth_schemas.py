from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from fastapi import Request, Form


class RegisterUserSchema(BaseModel):

    email: EmailStr = Field(..., example="user@example.com")
    username: str = Field(..., example="username123")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    password: str = Field(..., example="password")
    password2: str = Field(..., example="password")

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        username: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        password: str = Form(...),
        password2: str = Form(...),
    ):
        return cls(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            password2=password2,
        )
        


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
