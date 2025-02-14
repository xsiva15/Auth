from .interface import TablesRepositoryInterface
from .CommonTools import CommonTools
from sqlalchemy import update
from src.database import User
import uuid


class RecoveryRepo(TablesRepositoryInterface, CommonTools):
    async def update_password(self,
                              user_id: str,
                              new_password_hash: str
                              ) -> None:
        async with self._session_getter() as session:
            await session.execute(
                update(User)
                .where(User.id == uuid.UUID(user_id))
                .values(password_hash=new_password_hash)
            )