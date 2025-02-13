from src.repository.interface import TablesRepositoryInterface
from sqlalchemy import select
from src.database import User


class LoginRepo(TablesRepositoryInterface):
    async def find_user_by_email(self, email: str) -> User | None:

        async with self._session_getter() as session:
            result = await session.execute(
                    select(User).where(User.email == email)
                    )
            rows = result.scalars().all()

            if len(rows) == 0:
                return None
            else:
                # Мы исходим из логики один email == один юзер
                return rows[0]
