from fastapi import APIRouter, Depends
from src.models import (LoginResponse,
                        BadLoginResponse,
                        NoUserResponse,
                        LoginData,
                        DataForLogin)
from src.service import get_login_service

login_router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@login_router.post(
    "/",
    response_model=LoginResponse,
    summary="Ручка для логина юзера",
    responses={
        403: {"model": BadLoginResponse, 'detail': "Fail to login user"},
        404: {"model": NoUserResponse, "detail": "No such user"}
    }
)
async def login_user(data_for_login: DataForLogin,
                     service = Depends(get_login_service)
                     ) -> LoginResponse:
    return await service.login_user(
        LoginData(
            email=data_for_login.email,
            password=data_for_login.password
        )
    )