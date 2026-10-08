"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from copy import copy

from .clicker import AbstractClicker
from .exceptions import (
    GameWin,
    NoFoodError,
    NoMedicineError,
    NotEnoughMoney,
    TamagochiIsGone,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Инициализация класса игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Логика действия «работа».

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Логика действия «покупка еды»."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Логика действия «покупка лекарства»."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Логика действия «покормить питомца»."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Логика действия «вылечить питомца»."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Логика действия «отдохнуть»."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Логика действия «поиграть с питомцем»."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, int]:
        """
        Получение статуса игры.

        :return: словарь со всеми характеристиками
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Свойство для доступа к еде.

        :return: список еды в сумке
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Свойство для доступа к лекарствам.

        :return: список лекарств в сумке
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Реализация игры Тамагочи."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Инициализирует игру.

        :param tamagochi: Питомец.
        :param clicker: Кликер.
        :param all_food: Список доступной еды.
        :param all_medicine: Список доступных лекарств.
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []
        self._coins = 0

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """Питомец (только для чтения)."""
        return self._tamagochi

    @property
    def clicker(self) -> AbstractClicker:
        """Кликер (только для чтения)."""
        return self._clicker

    @property
    def available_food(self) -> list[Food]:
        """Доступная для покупки еда."""
        return self._all_food

    @property
    def available_medicine(self) -> list[Medicine]:
        """Доступные для покупки лекарства."""
        return self._all_medicine

    def _check_state(self) -> None:
        """
        Проверяет состояние питомца после действия.

        :raises TamagochiIsGone: если питомец умер
        :raises GameWin: если питомец полностью счастлив
        """
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone('Питомец умер')
        if self._tamagochi.is_happy():
            raise GameWin('Питомец счастлив — вы победили!')

    def work(self) -> int:
        """
        Пойти на работу — кликнуть и получить монеты.

        :return: Сколько монет заработано за клик.
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        self._check_state()
        return income

    def buy_food(self, index: int = 0) -> None:
        """
        Купить еду по индексу из списка доступной.

        :param index: Индекс еды в списке доступной.
        :raises NotEnoughMoney: если не хватает монет
        :raises IndexError: если такого продукта нет
        """
        if not self._all_food:
            return
        if not 0 <= index < len(self._all_food):
            raise IndexError('Такой еды нет в магазине')
        food = self._all_food[index]
        if self._coins < food.price:
            raise NotEnoughMoney('Недостаточно монет для покупки еды')
        self._coins -= food.price
        self._food_bag.append(food)
        self._tamagochi.update()
        self._check_state()

    def buy_medicine(self, index: int = 0) -> None:
        """
        Купить лекарство по индексу из списка доступных.

        :param index: Индекс лекарства в списке доступных.
        :raises NotEnoughMoney: если не хватает монет
        :raises IndexError: если такого лекарства нет
        """
        if not self._all_medicine:
            return
        if not 0 <= index < len(self._all_medicine):
            raise IndexError('Такого лекарства нет в магазине')
        medicine = self._all_medicine[index]
        if self._coins < medicine.price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства'
            )
        self._coins -= medicine.price
        self._medicine_bag.append(copy(medicine))
        self._tamagochi.update()
        self._check_state()

    def feed_tamagochi(self, index: int = 0) -> None:
        """
        Покормить питомца едой по индексу из сумки.

        :param index: Индекс еды в сумке.
        :raises NoFoodError: если сумка с едой пуста
        :raises IndexError: если такой еды нет в сумке
        """
        if not self._food_bag:
            raise NoFoodError('Кормить нечем — сумка с едой пуста')
        if not 0 <= index < len(self._food_bag):
            raise IndexError('Такой еды нет в сумке')
        food = self._food_bag.pop(index)
        self._tamagochi.feed(food)
        self._tamagochi.update()
        self._check_state()

    def heal_tamagochi(self, index: int = 0) -> None:
        """
        Вылечить питомца лекарством по индексу из сумки.

        :param index: Индекс лекарства в сумке.
        :raises NoMedicineError: если сумка с лекарствами пуста
        :raises IndexError: если такого лекарства нет в сумке
        """
        if not self._medicine_bag:
            raise NoMedicineError(
                'Лечить нечем — сумка с лекарствами пуста'
            )
        if not 0 <= index < len(self._medicine_bag):
            raise IndexError('Такого лекарства нет в сумке')
        medicine = self._medicine_bag[index]
        if medicine.is_empty():
            self._medicine_bag.pop(index)
            raise NoMedicineError('Лекарство закончилось')
        self._tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine_bag.pop(index)
        self._tamagochi.update()
        self._check_state()

    def rest_tamagochi(self) -> None:
        """Дать питомцу отдохнуть."""
        self._tamagochi.rest()
        self._tamagochi.update()
        self._check_state()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        self._tamagochi.play()
        self._tamagochi.update()
        self._check_state()

    def get_status(self) -> dict[str, int]:
        """
        Возвращает статус игры.

        :return: Словарь с характеристиками питомца и монетами.
        """
        status = dict(self._tamagochi.status)
        status['coins'] = self._coins
        status['is_sick'] = int(self._tamagochi.is_sick())
        return status

    @property
    def food(self) -> list[Food]:
        """Еда в сумке."""
        return self._food_bag

    @property
    def medicine(self) -> list[Medicine]:
        """Лекарства в сумке."""
        return self._medicine_bag
