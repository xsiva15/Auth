from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import RedirectResponse
from src.models import (
    EmailData,
    DataForSendingEmail,
    NoEmailInDataBase,
    convert_data_to_DataForReset,
    ResetExpired
    )
from src.service import get_recovery_service


recovery_router = APIRouter(
    prefix="/recover",
    tags=["recover"]
)


@recovery_router.put(
    "/new_password",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=RedirectResponse,
    summary="Используется для изменения текущего пароля пользователя, вся необходимая информация о пользователе передается через токен",
    responses={
        400: {"model": ResetExpired, "detail": "A link for recover was expired"}
    }
)
async def set_new_password(
        token: str,
        password: str,
        service=Depends(get_recovery_service)
):
    """
    Данная ручка должна быть использована на странице для обновления пароля, токен берется
    с пути к странице.
    Возвращает код 400 если токен уже не действует.
    """
    return await service.password_recover(
        convert_data_to_DataForReset(
            token=token,
            new_password=password
        )
    )



@recovery_router.post(
    "/send_email_for_new_password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Используется для отправки пользователю письма с ссылкой на страницу для сброса пароля",
    responses={
        404: {"model": NoEmailInDataBase, "detail": "No such user"}
    }
)
async def send_email_for_recov(
        email_data: EmailData,
        service=Depends(get_recovery_service)
):
    """
    Данная ручка используется для запроса отправки на указанный email ссылки на страницу,
    на которой можно будет восстановить пароль
    Возвращает 404 если такого пользователя нет.
    Возвращает 422 если введенный email некорректен
    """
    return await service.send_email_for_recov(
        DataForSendingEmail(
            email=email_data.email
        )
    )
