from sqlalchemy.orm import Session
from sqlalchemy import select, Result, desc

from app.core.models.users import Users



class AuthService:
    def __init__(self, session: Session):
        self.session = session


    def authenticate_user_db(self, username: str):
        stmt = select(Users).where(Users.username == username)
        result: Result = self.session.scalar(stmt)
        return result
    
    def get_user_by_id(self, user_id: int):
        stmt = select(Users).where(Users.id == user_id)
        result: Result = self.session.scalar(stmt)
        return result
    

    def validate_username(self, username: str):
        stmt = select(Users).where(Users.username == username)
        result: Result = self.session.execute(stmt)
        return result.first()
    

    def validate_email(self, email: str):
        stmt = select(Users).where(Users.email == email)
        result: Result = self.session.execute(stmt)
        return result.first()
    
    def create_user_db(self, user: Users):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    
