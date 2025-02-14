from fastapi import HTTPException, status
from src.models import (DataForSendingEmail,
                        DataForReset)
from src.repository import RecoveryRepo
from .MailService import MailService
from src.utils import PasswordManager


def get_recovery_service() -> "RecoveryService":
    return RecoveryService(repo=RecoveryRepo())


class RecoveryService(MailService):
    def __init__(self, repo: RecoveryRepo) -> None:
        self._repo = repo
        super().__init__()

    async def send_email_for_recov(self,
                                   email_data: DataForSendingEmail
                                   ) -> None:
        user_data = await self._repo.find_user_by_email(
            email=email_data.email
        )
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such user"
            )

        await self.send_reset_mail(
            user_id=str(user_data.id),
            email=email_data.email
        )

    async def password_recover(self, data_for_recover: DataForReset) -> None:
        if data_for_recover.expired:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A link for recover was expired"
            )

        password_hashed = PasswordManager.hash_password(
            data_for_recover.new_password
        )

        await self._repo.update_password(
            data_for_recover.user_id,
            password_hashed
        )

