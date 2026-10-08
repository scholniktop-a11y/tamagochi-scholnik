"""Модуль с интерфейсом и реализацией класса тамагочи."""

from abc import ABC, abstractmethod
from random import randint

from .models import Food, Medicine

# Границы показателей:
MIN_STAT = 0
MAX_STAT = 100

# Начальные значения питомца:
START_HUNGER = 50
START_HP = 100
START_ENERGY = 50
START_FATIGUE = 30

# Изменения показателей при действиях:
FEED_FATIGUE_DECREASE = 2
PLAY_ENERGY_COST = 10
PLAY_FATIGUE_DECREASE = 5
PLAY_HUNGER_INCREASE = 5
REST_ENERGY_GAIN = 20
REST_FATIGUE_DECREASE = 10
REST_SICK_ENERGY_GAIN = 10
REST_SICK_FATIGUE_DECREASE = 5

# Изменения при обновлении состояния:
UPDATE_HUNGER_GROWTH = 1
UPDATE_FATIGUE_GROWTH = 1
UPDATE_SICK_HUNGER_GROWTH = 2
UPDATE_SICK_FATIGUE_GROWTH = 3
UPDATE_SICK_HP_DECREASE = 5

# Порог болезни и шанс:
SICK_THRESHOLD = 90
SICK_CHANCE = 30
SICK_RANDINT_MAX = 100

# Условия счастья:
HAPPY_HP = 80
HAPPY_ENERGY = 50
HAPPY_HUNGER = 30
HAPPY_FATIGUE = 30


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
        self._name = name
        self._hunger = START_HUNGER
        self._hp = START_HP
        self._energy = START_ENERGY
        self._fatigue = START_FATIGUE
        self._sick = False

    def feed(self, food: Food) -> None:
        """
        Кормит питомца. Голод падает на величину сытости еды.

        :param food: Объект еды.
        """
        self._hunger = max(MIN_STAT, self._hunger - food.satiety)
        self._fatigue = max(
            MIN_STAT, self._fatigue - FEED_FATIGUE_DECREASE
        )

    def play(self) -> None:
        """Играет с питомцем: тратит энергию, снижает усталость."""
        self._energy = max(
            MIN_STAT, self._energy - PLAY_ENERGY_COST
        )
        self._fatigue = max(
            MIN_STAT, self._fatigue - PLAY_FATIGUE_DECREASE
        )
        self._hunger = min(
            MAX_STAT, self._hunger + PLAY_HUNGER_INCREASE
        )

    def rest(self) -> None:
        """Питомец отдыхает: восстанавливает энергию, снижает усталость."""
        if self._sick:
            self._energy = min(
                MAX_STAT, self._energy + REST_SICK_ENERGY_GAIN
            )
            self._fatigue = max(
                MIN_STAT,
                self._fatigue - REST_SICK_FATIGUE_DECREASE,
            )
        else:
            self._energy = min(
                MAX_STAT, self._energy + REST_ENERGY_GAIN
            )
            self._fatigue = max(
                MIN_STAT, self._fatigue - REST_FATIGUE_DECREASE
            )

    def heal(self, medicine: Medicine) -> None:
        """
        Лечит питомца.

        :param medicine: Объект лекарства.
        """
        if medicine.is_empty():
            return
        self._hp = min(MAX_STAT, self._hp + medicine.heal_hp)
        medicine.uses += 1
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Возвращает показатели питомца."""
        return {
            'hunger': self._hunger,
            'hp': self._hp,
            'energy': self._energy,
            'fatigue': self._fatigue,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        return self._hp > MIN_STAT

    def is_sick(self) -> bool:
        """Проверяет, болен ли питомец."""
        return self._sick

    def is_happy(self) -> bool:
        """
        Проверяет, полностью ли счастлив питомец.

        :return: True если все показатели в норме.
        """
        return (
            self._hp >= HAPPY_HP
            and self._energy >= HAPPY_ENERGY
            and self._hunger <= HAPPY_HUNGER
            and self._fatigue <= HAPPY_FATIGUE
            and not self._sick
        )

    def update(self) -> None:
        """Обновляет состояние питомца (голод, усталость, болезнь)."""
        hunger_growth = UPDATE_HUNGER_GROWTH
        fatigue_growth = UPDATE_FATIGUE_GROWTH

        if self._sick:
            hunger_growth += UPDATE_SICK_HUNGER_GROWTH
            fatigue_growth += UPDATE_SICK_FATIGUE_GROWTH
            self._hp = max(
                MIN_STAT, self._hp - UPDATE_SICK_HP_DECREASE
            )

        self._hunger = min(
            MAX_STAT, self._hunger + hunger_growth
        )
        self._fatigue = min(
            MAX_STAT, self._fatigue + fatigue_growth
        )

        is_critical = (
            self._hunger >= SICK_THRESHOLD
            or self._fatigue >= SICK_THRESHOLD
        )
        if is_critical and randint(1, SICK_RANDINT_MAX) <= SICK_CHANCE:
            self._sick = True
