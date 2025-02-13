from pydantic import BaseModel
from .EmailPreparator import EmailPreparator


class LoginData(EmailPreparator):
    email: str
    password: str

