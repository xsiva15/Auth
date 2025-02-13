from dataclasses import dataclass, field
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=
            Path.cwd().parent / ".env"
            )


@dataclass(frozen=True)
class SMTPParams:
    host = "smtp.timeweb.ru"
    port = 465
    SMTP_USER = "no-reply@asclavia.net"
    SMTP_PASSWORD = os.environ["EmailPassword"]


@dataclass(frozen=True)
class PasswordHashParam:
    rounds: int = 12


@dataclass(frozen=True)
class JwtTokenParams:
    """
    Время жизни токена для фронта в минутах и прочие параметры
    """
    access_lifespan = 1
    refresh_lifespan = 15
    secret_key = "blablabla"


@dataclass(frozen=True)
class DatabaseConfig:
    """Database connection variables."""

    name: str = 'mydatabase'
    user: str = 'myuser'
    password: str = "mypassword"
    port: int = 5432
    host: str = 'localhost'

    driver: str = 'asyncpg'
    database_system: str = 'postgresql'

    def build_connection_str(self) -> str:
        """This function build a connection string."""

        return URL.create(
            drivername=f'{self.database_system}+{self.driver}',
            username=self.user,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass(frozen=True)
class AppConfig:
    """App configuration."""

    title = "Auth app"
    description = "Smth"
    version = "1.0"
    root_path = ""


@dataclass(frozen=True)
class Configuration:
    app: AppConfig = field(default_factory=AppConfig)
    jwt_param: JwtTokenParams = field(default_factory=JwtTokenParams)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    password_hash_param: PasswordHashParam = field(default_factory=PasswordHashParam)


configuration = Configuration()
