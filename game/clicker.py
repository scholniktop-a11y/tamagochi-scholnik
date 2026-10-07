"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Свойство для доступа к количеству монет за клик."""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер с фиксированной случайной ставкой за клик."""

    def __init__(self) -> None:
        """Инициализирует кликер со случайной ставкой за клик."""
        self._income_per_click = randint(5, 15)
        self.clicks_count = 0

    @property
    def income_per_click(self) -> int:
        """Количество монет за один клик."""
        return self._income_per_click

    def click(self) -> None:
        """Фиксирует клик игрока."""
        self.clicks_count += 1
