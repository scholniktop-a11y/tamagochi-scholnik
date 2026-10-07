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
    """Кликер, накапливающий монеты за клик."""

    def __init__(self) -> None:
        """Инициализирует кликер с нулевым балансом."""
        self._income = 0

    @property
    def income_per_click(self) -> int:
        """Количество накопленных монет."""
        return self._income

    def click(self) -> None:
        """Накапливает случайное количество монет за клик."""
        self._income += randint(5, 15)

    def take_all_coins(self) -> int:
        """
        Забирает все накопленные монеты и обнуляет счётчик.

        :return: Количество монет.
        """
        coins = self._income
        self._income = 0
        return coins
