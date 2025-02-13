from pydantic import BaseModel
from .EmailPreparator import EmailPreparator


class RegistrationData(EmailPreparator):
    phone: int
    email: str
    password: str
