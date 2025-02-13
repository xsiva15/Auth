from .interface import TablesRepositoryInterface
from src.database import User
from sqlalchemy import insert, select, update, exists
from datetime import datetime, timezone


class RegistrationRepo(TablesRepositoryInterface):
    async def add_user(self,
                       email: str,
                       phone_num: str,
                       password_hash: str
                       ) -> None:
        async with self._session_getter() as session:
            await session.execucute(
                insert(User).values(
                    username=email,
                    email=email,
                    password_hash=password_hash,
                    phone_number=phone_num,
                    is_active=False,
                    created_at=datetime.now(timezone.utc)
                )
            )

    async def is_user_exists(self,
                             email: str
                             ) -> bool:
        """
        True если этот пользователь уже существует, False иначе
        """
        async with self._session_getter() as session:
            result = await session.execute(
                    select(exists().where(User.email == email))
                    )
            return result.scalar()

    async def make_users_email_verified(self,
                                        email: str
                                        ) -> None:
        async with self._session_getter() as session:
            await session.execute(
                update(User)
                .where(User.email == email)
                .values(is_active=True)
            )
