import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class DatabaseConfig:
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "12345")
    host: str = os.getenv("DB_HOST", "localhost")
    name: str = os.getenv("DB_NAME", "tasks")
    port: int = int(os.getenv("DB_PORT", 5432))
    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class TestDatabaseConfig(DatabaseConfig):
    name: str = os.getenv("TEST_DB_NAME", "tasks_test")


class AuthConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class Settings:
    db = DatabaseConfig()
    auth = AuthConfig()
    test_db = TestDatabaseConfig()


settings = Settings()
