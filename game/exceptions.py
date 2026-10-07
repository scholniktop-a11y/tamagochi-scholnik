"""Модуль с исключениями."""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи."""


class NotEnoughMoney(Exception):
    """Ошибка когда не хватает монет для покупки."""


class GameWin(Exception):
    """Игрок выиграл."""


class NoFoodError(Exception):
    """Ошибка когда в сумке нет еды."""


class NoMedicineError(Exception):
    """Ошибка когда в сумке нет лекарств."""
