from pydantic import BaseModel
from src.utils import ResetPassManager
from fastapi import HTTPException, status


class DataForReset(BaseModel):
    user_id: str
    email: str
    expired: bool
    new_password: str


def convert_data_to_DataForReset(
        token: str,
        new_password: str
) -> DataForReset:

    dec_data = ResetPassManager.decode_token(
        token
    )

    if dec_data is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The token is invalid"
        )

    return DataForReset(
        user_id=dec_data["user"],
        email=dec_data["email"],
        expired=dec_data["expired"],
        new_password=new_password
    )
