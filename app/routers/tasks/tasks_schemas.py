from datetime import date
from typing import Annotated
from pydantic import BaseModel
from fastapi import Form


class TaskCreateSchema(BaseModel):
    date_task: str
    description: str
    duration_minutes: int

    @classmethod
    def as_form(
        cls,
        date_task: Annotated[str, Form(..., alias="date_task")],
        description: Annotated[str, Form(..., alias="description")],
        duration_minutes: Annotated[int, Form(..., alias="duration_minutes")],
    ) -> "TaskCreateSchema":
        return cls(date_task=date_task, description=description, duration_minutes=duration_minutes)
