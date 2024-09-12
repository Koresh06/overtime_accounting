import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.core.base import Base
from app.core.models import Users, Tasks
from app.core.db_halper import test_db_helper
from app.utils.assistants_auth import bcrypt_context
from app.__main__ import app



def override_get_current_user():
    return {"username": "test", "id": 1, "role": "admin"}


client = TestClient(app)


@pytest.fixture
def test_task():
    task = Tasks(
        user_id = 1,
        date_task = "2022-01-01",
        description = "test",
        time_interval = 30,
    )

    session = test_db_helper.get_db()
    session.add(task)
    session.commit()
    session.refresh(task)

    yield task

    with test_db_helper.get_session() as conn:
        conn.delete(task)
        conn.commit()

