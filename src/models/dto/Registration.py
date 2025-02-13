from pydantic import BaseModel


class RegistrationData(BaseModel):
    phone: int
    email: str
    password: str
