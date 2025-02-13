from pydantic import BaseModel, field_validator
from email_validator import validate_email


class EmailNormalizer(BaseModel):
    @field_validator("email", check_fields=False)
    def check_is_email_valid(cls, email: str) -> str:
        return validate_email(
                email.strip(),
                check_deliverability=False,
                allow_smtputf8=False,
        ).normalized
