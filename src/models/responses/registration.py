from pydantic import BaseModel, field_validator
from starlette import status


class RegistrationResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class SuchUserExists(BaseModel):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "Such user already exists"


class UserData(BaseModel):
    phone: str
    email: str
    password: str

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        # Удаляем '+' в начале, если есть
        value = value.lstrip('+')

        if not value.isdigit():
            raise ValueError("Номер телефона должен содержать только цифры.")

        return value
