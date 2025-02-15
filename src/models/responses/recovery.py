from pydantic import BaseModel
from .EmailNormaliztion import EmailNormalizer
from starlette import status


class EmailData(EmailNormalizer):
    email: str


class DataForSendingEmail(BaseModel):
    email: str


class ResetExpired(BaseModel):
    status_code: int = status.HTTP_400_BAD_REQUEST,
    detail: str = "A link for recover was expired"


class NoEmailInDataBase(BaseModel):
    status_code: int = status.HTTP_404_NOT_FOUND,
    detail: str = "User not found in database"


class BadTokenResponse(BaseModel):
    status_code: int = status.HTTP_403_FORBIDDEN,
    detail: str = "The token is invalid"