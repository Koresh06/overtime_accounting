from typing import Generator
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


from app.config import DatabaseConfig, settings


class DatabaseHelper:
    
    def __init__(self, config: DatabaseConfig):
        self.config = config

    def get_engine(self) -> Engine:
        return create_engine(
            url=self.config.url,
            echo=self.config.echo,
        )

    def get_session(self) -> sessionmaker:
        return sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self.get_engine(),
        )
    
    def get_db(self) -> Generator:
        SessionLocal = self.get_session()
        db = SessionLocal()  # Создание сессии
        try:
            yield db
        finally:
            db.close()  # Закрытие сессии


db_helper = DatabaseHelper(config=settings.db)
test_db_helper = DatabaseHelper(config=settings.test_db)