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
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_user: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    task_rel: Mapped["Tasks"] = relationship(back_populates="user_rel", cascade="all, delete")


    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username}, first_name={self.first_name}, last_name={self.last_name}, is_active={self.is_active}, is_user={self.is_user}, is_admin={self.is_admin}, is_super_admin={self.is_super_admin}>"