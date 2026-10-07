"""Модуль с интерфейсом и реализацией класса тамагочи."""

from abc import ABC, abstractmethod
from random import randint

from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи.

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи.

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Свойство для доступа ко всем состояниям тамагочи.

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Проверяет, жив ли тамагочи.

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Проверяет, болен ли тамагочи.

        :return: True если болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_happy(self) -> bool:
        """
        Проверяет, полностью ли счастлив тамагочи.

        :return: True если счастлив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Обновляет состояния тамагочи.

        Должен вызываться после каждого действия.
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Простая реализация питомца."""

    def __init__(self, name: str = 'Питомец') -> None:
        """
        Инициализирует питомца.

        :param name: Имя питомца.
        """
        self.name = name
        self.hunger = 50
        self.hp = 100
        self.energy = 50
        self.fatigue = 0
        self._sick = False

    def feed(self, food: Food) -> None:
        """
        Кормит питомца. Голод падает на величину сытости еды.

        :param food: Объект еды.
        """
        self.hunger = max(0, self.hunger - food.satiety)

    def play(self) -> None:
        """Играет с питомцем: тратит энергию, снижает усталость."""
        self.energy = max(0, self.energy - 10)
        self.fatigue = max(0, self.fatigue - 10)
        self.hunger = min(100, self.hunger + 5)

    def rest(self) -> None:
        """Питомец отдыхает: восстанавливает энергию."""
        if self._sick:
            self.energy = min(100, self.energy + 10)
            self.fatigue = max(0, self.fatigue - 5)
        else:
            self.energy = min(100, self.energy + 20)
            self.fatigue = max(0, self.fatigue - 10)

    def heal(self, medicine: Medicine) -> None:
        """
        Лечит питомца.

        :param medicine: Объект лекарства.
        """
        if medicine.is_empty():
            return
        self.hp = min(100, self.hp + medicine.heal_hp)
        medicine.uses += 1
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Возвращает показатели питомца."""
        return {
            'hunger': self.hunger,
            'hp': self.hp,
            'energy': self.energy,
            'fatigue': self.fatigue,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        return self.hp > 0

    def is_sick(self) -> bool:
        """Проверяет, болен ли питомец."""
        return self._sick

    def is_happy(self) -> bool:
        """
        Проверяет, полностью ли счастлив питомец.

        :return: True если все показатели в норме.
        """
        return (
            self.hp >= 100
            and self.energy >= 80
            and self.hunger <= 20
            and self.fatigue <= 20
            and not self._sick
        )

    def update(self) -> None:
        """Обновляет состояние питомца (голод, усталость, болезнь)."""
        hunger_growth = 1
        fatigue_growth = 1

        if self._sick:
            hunger_growth += 2
            fatigue_growth += 3
            self.hp = max(0, self.hp - 5)

        self.hunger = min(100, self.hunger + hunger_growth)
        self.fatigue = min(100, self.fatigue + fatigue_growth)

        is_critical = self.hunger >= 90 or self.fatigue >= 90
        if is_critical and randint(1, 100) <= 30:
            self._sick = True
