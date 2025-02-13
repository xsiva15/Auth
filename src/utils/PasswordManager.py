from passlib.context import CryptContext
from src.config import configuration

class PasswordHasher:
    """ Класс-обёртка для работы с Passlib (bcrypt). """

    def __init__(self, rounds: int = 12):
        """
        :param rounds: число «раундов» (cost) для bcrypt.
        """
        self._pwd_context = CryptContext(
            schemes=["bcrypt"],
            default="bcrypt",
            bcrypt__rounds=rounds
        )

    def hash_password(self, password: str) -> str:
        """
        Вернёт хэш пароля в виде строки, включая соль и идентификатор алгоритма.
        """
        return self._pwd_context.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Проверяет, что 'password' соответствует хэшу 'hashed'.
        """
        return self._pwd_context.verify(password, hashed)

    def needs_rehash(self, hashed: str) -> bool:
        """
        Проверка, нужен ли ре-хэш (обновление хэша) при изменении политики (например, rounds).
        """
        return self._pwd_context.needs_update(hashed)


PasswordManager = PasswordHasher(
    rounds=configuration.password_hash_param.rounds
)