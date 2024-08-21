from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from app.utils.case_convector import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}"