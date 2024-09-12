from typing import List, TYPE_CHECKING
from datetime import datetime, date
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base import Base

if TYPE_CHECKING: 
    from app.core.models.users import Users


class Tasks(Base):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_task: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    time_interval: Mapped[int] = mapped_column(Integer)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    status: Mapped[bool] = mapped_column(Boolean, default=False)

    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


    user_rel: Mapped[List["Users"]] = relationship(back_populates="task_rel")

    def __repr__(self):
        return f"<Task(id={self.id}, user_id={self.user_id}, date={self.date_task}, description={self.description}, time_interval={self.time_interval}, create_at={self.create_at}, update_at={self.update_at}, status={self.status})>"