"""Точка входа в игру Тамагочи."""

import os

from game.clicker import SimpleRandomClicker
from game.exceptions import (
    GameWin,
    NoFoodError,
    NoMedicineError,
    NotEnoughMoney,
    TamagochiIsGone,
)
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi

# Шаблон отображения сумок:
BAG_TEMPLATE = (
    'Сумка с едой: {food}\n'
    'Сумка с лекарствами: {medicine}'
)

# Шаблон отображения статуса питомца:
STATUS_TEMPLATE = (
    '\nСтатус: голод {hunger}, здоровье {hp}, '
    'энергия {energy}, усталость {fatigue}, монет {coins}\n'
)

# Сообщение о болезни:
SICK_MESSAGE = (
    '=======Тамагочи болеет======\n'
    '===Отдых действует менее эффективно==='
)

# Меню действий:
MENU = '\n'.join([
    '1. Пойти на работу',
    '2. Купить еду',
    '3. Купить лекарство',
    '4. Покормить',
    '5. Вылечить',
    '6. Играть',
    '7. Отдых',
    '0. Выход',
])


def clear_console() -> None:
    """Очищает консоль в зависимости от ОС."""
    os.system('cls' if os.name == 'nt' else 'clear')


def choose_index(items: list, item_name: str) -> int:
    """
    Показывает список товаров и предлагает выбрать номер.

    :param items: Список доступных товаров.
    :param item_name: Название категории (для подсказки).
    :return: Выбранный индекс (0-based) или -1, если выбор отменён.
    """
    print('\nДоступные варианты ({}):'.format(item_name))
    for i, item in enumerate(items):
        print(f'{i + 1}. {item}')
    choice = input('Введите номер (или Enter для отмены): ').strip()
    if not choice:
        return -1
    if not choice.isdigit():
        return -1
    number = int(choice)
    if not 1 <= number <= len(items):
        return -1
    return number - 1


def main() -> None:
    """Основной игровой цикл."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(
            name='Ибупрофен',
            price=30,
            heal_hp=20,
            number_of_uses=2,
        ),
        Medicine(
            name='Аспирин',
            price=20,
            heal_hp=15,
            number_of_uses=3,
        ),
        Medicine(
            name='Витамины',
            price=15,
            heal_hp=10,
            number_of_uses=5,
        ),
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker()
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print('Добро пожаловать в Тамагочи-кликер!')
    output = ''

    while True:
        print(output)

        print(BAG_TEMPLATE.format(
            food=game.food,
            medicine=game.medicine,
        ))

        status = game.get_status()
        print(STATUS_TEMPLATE.format(**status))

        if status['is_sick']:
            print(SICK_MESSAGE)

        print(MENU)

        try:
            match input('Выберите действие: '):
                case '1':
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                case '2':
                    index = choose_index(game.available_food, 'еда')
                    if index < 0:
                        output = 'Покупка отменена'
                    else:
                        game.buy_food(index)
                        output = 'Еда куплена'
                case '3':
                    index = choose_index(
                        game.available_medicine, 'лекарства'
                    )
                    if index < 0:
                        output = 'Покупка отменена'
                    else:
                        game.buy_medicine(index)
                        output = 'Лекарство куплено'
                case '4':
                    index = choose_index(game.food, 'еда в сумке')
                    if index < 0:
                        output = 'Кормление отменено'
                    else:
                        game.feed_tamagochi(index)
                        output = 'Питомец покормлен'
                case '5':
                    index = choose_index(
                        game.medicine, 'лекарства в сумке'
                    )
                    if index < 0:
                        output = 'Лечение отменено'
                    else:
                        game.heal_tamagochi(index)
                        output = 'Питомец вылечен'
                case '6':
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case '7':
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case '0':
                    print('До встречи!')
                    break
                case _:
                    output = 'Неверная команда'
        except NotEnoughMoney as error:
            output = f'Ошибка: {error}'
        except NoFoodError as error:
            output = f'Ошибка: {error}'
        except NoMedicineError as error:
            output = f'Ошибка: {error}'
        except IndexError as error:
            output = f'Ошибка: {error}'
        except TamagochiIsGone as error:
            print(f'\nИгра окончена: {error}')
            break
        except GameWin as error:
            print(f'\nПобеда! {error}')
            break

        clear_console()


if __name__ == '__main__':
    main()
