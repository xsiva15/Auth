import datetime
import jwt

from src.config import configuration


class JWTGenerator:
    def __init__(self,
                 access_lifespan: int,
                 refresh_lifespan: int,
                 secret_key: str
                 ) -> None:
        self._access_lifespan = access_lifespan
        self._refresh_lifespan = refresh_lifespan
        self.__secret_key = secret_key

    def generate_tokens(self, user_index: str, email: str) -> dict[str, str]:
        common_payl = {
            "user_id": user_index,
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self._access_lifespan)
        }

        access_jwt = jwt.encode(
            payload=common_payl | {
                "type": "Access",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self._access_lifespan)
            },
            key=self.__secret_key,
            algorithm="HS256"
        )

        refresh_jwt = jwt.encode(
            payload=common_payl | {
                "type": "Refresh",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self._refresh_lifespan)
            },
            key=self.__secret_key,
            algorithm="HS256"
        )

        return {"access": access_jwt, "refresh": refresh_jwt}


JWTManager = JWTGenerator(
    access_lifespan=configuration.jwt_param.access_lifespan,
    refresh_lifespan=configuration.jwt_param.refresh_lifespan,
    secret_key=configuration.jwt_param.secret_key
)

