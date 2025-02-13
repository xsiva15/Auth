from abc import ABC
from typing import Callable, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session


class TablesRepositoryInterface(ABC):

    __slots__ = ('_session_getter', 'model',)

    def __init__(self, session_getter: Callable[[], AsyncGenerator[AsyncSession, None]] = get_session) -> None:
        """
        :session_getter Нужно передать коннектор к базе данных
        """
        self._session_getter: Callable[[], AsyncGenerator[AsyncSession, None]] = session_getter