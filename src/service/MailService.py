import asyncio
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import configuration
from src.utils import ResetPassManager, ConfirmUrlManager
from src.logger import mail_logger
from fastapi_mail.errors import ConnectionErrors

connection_config = ConnectionConfig(
    MAIL_USERNAME=configuration.smtp_params.user,
    MAIL_PASSWORD=configuration.smtp_params.password,
    MAIL_FROM=configuration.smtp_params.user,
    MAIL_PORT=configuration.smtp_params.port,
    MAIL_SERVER=configuration.smtp_params.host,
    MAIL_SSL_TLS=configuration.smtp_params.port == 465,
    MAIL_STARTTLS=configuration.smtp_params.port == 587,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

fast_mail = FastMail(connection_config)


"""
url_to_go --- ссылка по которой должен перейти юзер в данном письме, чтобы перевести  
содержимое письма на HTML вставляйте его в body и также измените 
subtype на MessageType.HTML 
"""


class MailService:
    def __init__(self, mail_app: FastMail = fast_mail) -> None:
        self._mail_app = mail_app

    async def _send_message_with_retry_and_log(self,
                                               message: MessageSchema,
                                               retry: int = 5,
                                               delay: float = 1) -> None:
        num_bad = 0
        while num_bad <= retry:
            try:
                await self._mail_app.send_message(message)
                return None
            except ConnectionErrors:
                num_bad += 1
                if num_bad == 1:
                    mail_logger.warning(
                        f"Ошибка соединения при отправке письма {message.recipients[0]}"
                    )
                await asyncio.sleep(delay)

        mail_logger.error(
            f"Не удалось отправить сообщение пользователю {message.recipients[0]} из-за ошибки соединения"
        )

    async def send_user_confirm_mail(
            self,
            email: str,
            user_id: str
    ):
        url_to_go = ConfirmUrlManager.generate_confirm_email_link(
            email=email,
            user_id=user_id
        )
        message = MessageSchema(
            subject="Email confirmation",
            recipients=[email],
            body=url_to_go,
            subtype=MessageType.plain
        )

        await self._send_message_with_retry_and_log(message)

    async def send_reset_mail(self,
                              email: str,
                              user_id: str) -> None:
        url_to_go = ResetPassManager.generate_reset_link(
            email=email,
            user_id=user_id
        )
        message = MessageSchema(
            subject="Reset password",
            recipients=[email],
            body=url_to_go,
            subtype=MessageType.plain
        )
        await self._send_message_with_retry_and_log(message)


