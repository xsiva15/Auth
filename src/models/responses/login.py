from pydantic import BaseModel
from starlette import status
from .EmailNormaliztion import EmailNormalizer


class DataForLogin(EmailNormalizer):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class BadLoginResponse(BaseModel):
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Invalid data for login"


class NoUserResponse(BaseModel):
    status_code: int = status.HTTP_404_NOT_FOUND,
    detail: str = "User not found"