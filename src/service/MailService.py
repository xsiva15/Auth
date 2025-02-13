from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import configuration
from src.utils import ResetPassManager, ConfirmUrlManager

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


class MailService:
    def __init__(self, mail_app: FastMail = fast_mail) -> None:
        self._mail_app = mail_app

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
        await self._mail_app.send_message(message)

    async def send_reset_mail(self,
                              email: str,
                              user_id: str) -> None:
        url_to_go = ResetPassManager(
            email=email,
            user_id=user_id
        )
        message = MessageSchema(
            subject="Reset password",
            recipients=[email],
            body=url_to_go,
            subtype=MessageType.plain
        )
        await self._mail_app.send_message(message)


