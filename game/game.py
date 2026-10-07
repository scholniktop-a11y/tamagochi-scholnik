"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod

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
        self.tamagochi = tamagochi
        self.clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []
        self._coins = 0

    def _check_state(self) -> None:
        """
        Проверяет состояние питомца после действия.

        :raises TamagochiIsGone: если питомец умер
        :raises GameWin: если питомец полностью счастлив
        """
        if not self.tamagochi.is_alive():
            raise TamagochiIsGone('Питомец умер')
        if self.tamagochi.is_happy():
            raise GameWin('Питомец счастлив — вы победили!')

    def work(self) -> int:
        """
        Пойти на работу — кликнуть и забрать монеты.

        :return: Сколько монет заработано за клик.
        """
        self.clicker.click()
        income = self.clicker.take_all_coins()
        self._coins += income
        self.tamagochi.update()
        self._check_state()
        return income

    def buy_food(self) -> None:
        """
        Купить первую доступную еду.

        :raises NotEnoughMoney: если не хватает монет
        """
        if not self._all_food:
            return
        food = self._all_food[0]
        if self._coins < food.price:
            raise NotEnoughMoney('Недостаточно монет для покупки еды')
        self._coins -= food.price
        self._food_bag.append(food)
        self.tamagochi.update()
        self._check_state()

    def buy_medicine(self) -> None:
        """
        Купить первое доступное лекарство.

        :raises NotEnoughMoney: если не хватает монет
        """
        if not self._all_medicine:
            return
        medicine = self._all_medicine[0]
        if self._coins < medicine.price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства'
            )
        self._coins -= medicine.price
        self._medicine_bag.append(medicine)
        self.tamagochi.update()
        self._check_state()

    def feed_tamagochi(self) -> None:
        """
        Покормить питомца первой едой из сумки.

        :raises NoFoodError: если в сумке нет еды
        """
        if not self._food_bag:
            raise NoFoodError('Кормить нечем — сумка с едой пуста')
        food = self._food_bag.pop(0)
        self.tamagochi.feed(food)
        self.tamagochi.update()
        self._check_state()

    def heal_tamagochi(self) -> None:
        """
        Вылечить питомца первым непустым лекарством из сумки.

        :raises NoMedicineError: если в сумке нет лекарств
        """
        if not self._medicine_bag:
            raise NoMedicineError(
                'Лечить нечем — сумка с лекарствами пуста'
            )
        medicine = self._medicine_bag[0]
        if medicine.is_empty():
            self._medicine_bag.pop(0)
            raise NoMedicineError('Лекарство закончилось')
        self.tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine_bag.pop(0)
        self.tamagochi.update()
        self._check_state()

    def rest_tamagochi(self) -> None:
        """Дать питомцу отдохнуть."""
        self.tamagochi.rest()
        self.tamagochi.update()
        self._check_state()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        self.tamagochi.play()
        self.tamagochi.update()
        self._check_state()

    def get_status(self) -> dict[str, int]:
        """
        Возвращает статус игры.

        :return: Словарь с характеристиками питомца и монетами.
        """
        status = dict(self.tamagochi.status)
        status['coins'] = self._coins
        status['is_sick'] = int(self.tamagochi.is_sick())
        return status

    @property
    def food(self) -> list[Food]:
        """Еда в сумке."""
        return self._food_bag

    @property
    def medicine(self) -> list[Medicine]:
        """Лекарства в сумке."""
        return self._medicine_bag
