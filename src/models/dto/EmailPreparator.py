from pydantic import BaseModel, field_validator


class EmailPreparator(BaseModel):
    @field_validator("email", check_fields=False)
    def delete_bad_symbols(cls, email: str) -> str:
        return email.strip()