from fastapi import HTTPException, status
from src.repository import RegistrationRepo
from src.models import RegistrationResponse, RegistrationData
from src.utils import JWTManager, PasswordManager
from .MailService import MailService


def get_registration_service() -> "RegistrationService":
    return RegistrationService(repo=RegistrationRepo())


class RegistrationService(MailService):
    def __init__(self, repo: RegistrationRepo) -> None:
        self._repo = repo
        super().__init__()

    async def registrate_user(self,
                              registr_data: RegistrationData
                              ) -> RegistrationResponse:
        user_exists = await self._repo.is_user_exists(
            registr_data.email
        )
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Such user already exists"
            )

        hash_password = PasswordManager.hash_password(
            registr_data.password
        )

        user_id = await self._repo.add_user(
            email=registr_data.email,
            phone_num=str(registr_data.phone),
            password_hash=hash_password
        )

        tokens = JWTManager.generate_tokens(
            user_index=str(user_id),
            email=registr_data.email
        )

        await self.send_user_confirm_mail(
            email=registr_data.email,
            user_id=str(user_id)
        )

        return RegistrationResponse(
            access_token=tokens["access"],
            refresh_token=tokens["refresh"]
        )

    async def confirm_email(self):
        pass