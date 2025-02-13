from src.repository import RegistrationRepo


class RegistrationService:
    def __init__(self, repo: RegistrationRepo) -> None:
        self._repo = repo

    def registrate_user(self):
        pass

    def confirm_email(self):
        pass