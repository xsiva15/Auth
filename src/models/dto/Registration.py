from pydantic import BaseModel
from src.utils import ConfirmUrlManager


class RegistrationData(BaseModel):
    phone: int
    email: str
    password: str


class ConfirmationData(BaseModel):
    user_id: str
    email: str
    expired: bool


def convert_token_to_ConfirmationData(token: str) -> ConfirmationData:
    dec_data = ConfirmUrlManager.decode_token(
        token
    )
    return ConfirmationData(
        email=dec_data["email"],
        user_id=dec_data["user"],
        expired=dec_data["expired"]
    )