from src.repository import LoginRepo
from src.models import LoginData, LoginResponse
from src.utils import PasswordManager, JWTManager
from fastapi import HTTPException, status


def get_login_service() -> "LoginService":
    return LoginService(repository=LoginRepo())


class LoginService:
    def __init__(self, repository: LoginRepo) -> None:
        self._repo = repository

    async def login_user(self, login_data: LoginData) -> LoginResponse:
        user_data = await self._repo.find_user_by_email(
            login_data.email
        )
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such user"
            )

        password_check_result = PasswordManager.verify_password(
            login_data.password, user_data.password_hash
        )

        if password_check_result:
            tokens = JWTManager.generate_tokens(
                user_index=user_data.id,
                email=user_data.email
            )
            return LoginResponse(
                access_token=tokens["access"],
                refresh_token=tokens["refresh"]
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Fail to login user"
            )






