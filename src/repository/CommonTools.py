from sqlalchemy import select
from src.database import User
from sqlalchemy import exists


class CommonTools:
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

    async def verify_email_affiliation(self, email: str, user_id: str) -> bool:
        """
        Проверяет, что email принадлежит определенному id пользователя
        True если принадлежит False иначе
        """
        user_data = await self.find_user_by_email(email=email)

        if user_data is None:
            return False

        return str(user_data.id) == user_id


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

