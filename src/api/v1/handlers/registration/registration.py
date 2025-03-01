from fastapi import APIRouter, Depends
from src.models import (RegistrationResponse,
                        SuchUserExists,
                        UserData,
                        RegistrationData,
                        convert_token_to_ConfirmationData,
                        BadTokenResp
                        )
from src.service import get_registration_service
from starlette import status
from starlette.responses import RedirectResponse


registration_router = APIRouter(
    prefix="/registration",
    tags=["registration"]
)


@registration_router.post(
    path="/",
    response_model=RegistrationResponse,
    responses={409: {"model": SuchUserExists, 'detail': "You are already are a user, please login"}},
    summary="Регистрирует нового пользователя"

)
async def registrate_user(
        user_data: UserData,
        service = Depends(get_registration_service)
) -> RegistrationResponse:
    """
    Валидирует номер телефона и email на предмет их формата, если что то не
    так возвращается кож ошибки 422.
    Также может вернуть код ошибки 409 если пользователь уже есть в базе
    """

    return await service.registrate_user(
        RegistrationData(
            email=user_data.email,
            phone=int(user_data.phone),
            password=user_data.password
        )
    )


@registration_router.get(
    "/confirm-email",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=RedirectResponse,
    summary="Высылается пользователю на почту для подтверждения email",
    responses={
        403: {"model": BadTokenResp, 'detail': "The token is invalid"}
    }
)
async def confirm_email(
        token: str,
        service = Depends(get_registration_service)
):
    """
    Данная ручка будет задействована в ссылке для подтверждения email-а
    Логика такая: если токен в пиьме еще жив, то все гуд - перенапраляем чела на наш сайт, если нет на веб страницу
    где пишем, что отправили новое пиьмо
    """
    return await service.confirm_email(
        convert_token_to_ConfirmationData(token)
    )
