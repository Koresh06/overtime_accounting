from sqlalchemy.orm import Session
from sqlalchemy import select, Result, desc

from app.core.models.tasks import Tasks
from app.routers.schemas.tasks_schemas import TaskCreateSchema



class TasksService:
    def __init__(self, session: Session):
        self.session = session


    def get_all_tasks(self, user_id: int):
        stmt = select(Tasks).where(Tasks.user_id == user_id).order_by(desc(Tasks.id))
        result: Result = self.session.scalars(stmt)
        return result
    

    def create_task(self, task: TaskCreateSchema, user_id: int):
        task_model = Tasks(
            user_id=user_id,
            description=task.description,
            date_task=task.date_task,
            time_interval=task.duration_minutes,
        )
        self.session.add(task_model)
        self.session.commit()
        self.session.refresh(task_model)
