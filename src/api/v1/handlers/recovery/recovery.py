from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse



recovery_router = APIRouter(
    prefix="/recover",
    tags=["recover"]
)


@recovery_router.put(
    "/new_password",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=RedirectResponse,
    summary="Используется для изменения текущего пароля пользователя, вся необходимая информация о пользователе передается через токен"
)
async def set_new_password(
        token: str,
        password: str
):
    pass


@recovery_router.post(
    "/send_email_for_new_password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Используется для отправки пользователю письма с ссылкой на страницу для сброса пароля"
)
async def send_email_for_recov(email: str):
    pass