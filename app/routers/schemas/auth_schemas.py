from typing import Optional
from pydantic import BaseModel
from fastapi import Request


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "smail@.com",
                "username": "Smail_43",
                "first_name": "Smail",
                "last_name": "Smailov",
                "password": "12345",
                "role": "user",
            }
        }
    }


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
