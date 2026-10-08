"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod
from random import randint

# Константы для диапазона дохода за клик:
MIN_INCOME = 5
MAX_INCOME = 15


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
    """Кликер со случайным доходом за каждый клик."""

    def __init__(self) -> None:
        """Инициализирует кликер с нулевым доходом."""
        self._income_per_click = 0
        self._clicks_count = 0

    @property
    def income_per_click(self) -> int:
        """Количество монет, заработанных за последний клик."""
        return self._income_per_click

    def click(self) -> None:
        """Фиксирует клик и генерирует случайный доход за него."""
        self._clicks_count += 1
        self._income_per_click = randint(MIN_INCOME, MAX_INCOME)
