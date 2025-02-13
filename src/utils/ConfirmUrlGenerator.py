import datetime
import jwt
from typing import Any
from src.config import configuration


class ConfirmUrlGenerator:
    def __init__(self,
                 base_url: str,
                 secret_key: str,
                 lifespan: int) -> None:
        self._base_url = base_url
        self.__secret_key = secret_key
        self._lifespan = lifespan

    def generate_confirm_email_link(self,
                               email: str,
                               user_id: str) -> str:
        payl = {
            "user": user_id,
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self._lifespan)
        }
        token = jwt.encode(
            payload=payl,
            key=self.__secret_key,
            algorithm="HS256"
        )
        return self._base_url + f"/v1/registration/confirm-email?token={token}"

    def decode_token(self, token: str) -> dict[str, Any]:
        decoded_payload = jwt.decode(
            jwt=token,
            key=self.__secret_key,
            algorithms=["HS256"],
            options={"verify_exp": False}
        )

        return {el: decoded_payload[el] for el in ["user", "email"]} | {"expired": decoded_payload["exp"] < datetime.datetime.utcnow()}


ConfirmUrlManager = ConfirmUrlGenerator(
    base_url=configuration.confirm_email_params.base_url,
    secret_key=configuration.confirm_email_params.secret_key,
    lifespan=configuration.confirm_email_params.lifespan_m
)
