from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base import Base

if TYPE_CHECKING:
    from app.core.models.tasks import Tasks


class Users(Base):

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    task_rel: Mapped["Tasks"] = relationship(back_populates="user_rel", cascade="all, delete")


    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}), username={self.username}, first_name={self.first_name}, last_name={self.last_name}, role={self.role}, is_active={self.is_active}>"