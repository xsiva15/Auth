from fastapi import HTTPException, status
from src.repository import RegistrationRepo
from src.models import RegistrationResponse, RegistrationData, ConfirmationData
from src.utils import JWTManager, PasswordManager
from .MailService import MailService
from starlette.responses import RedirectResponse


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

    async def confirm_email(self,
                            conf_data: ConfirmationData) -> RedirectResponse:
        """
        Выполняет подтверждение email и редиректит на главную страницу сайта если,
        токен в ссылке еще жиа, если нет, то отправляет новую ссылку на почту и делает редирект на
        страницу где написано о том, что была выслана новая ссылка (пока такой страницы нет)
        """
        if conf_data.expired:
            await self.send_user_confirm_mail(
                email=conf_data.email,
                user_id=conf_data.user_id
            )
            # Тут должно быть перенаправление на страницу, где мы пишем о том, что
            # мы выслали челу новую ссылку
            return RedirectResponse(url="https://asclavia.net/")

        if await self._repo.verify_email_affiliation(conf_data.email, conf_data.user_id):
            await self._repo.make_users_email_verified(conf_data.email)

        else:
            pass
            # По хорошему тут бы залогировать

        return RedirectResponse(url="https://asclavia.net/")
