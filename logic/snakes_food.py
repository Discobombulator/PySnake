from constants import Constants
import random


def create_food_set(snake_body, obstacles, count=800):
    """create_food_set: Создает набор еды для змейки,
     исключая позиции змейки и препятствий."""

    food_set = set()
    while len(food_set) < count:
        pos = (
            random.randint(0, Constants.FIELD_HEIGHT - 1),
            random.randint(0, Constants.FIELD_WIDTH - 1)
        )
        if pos in snake_body or pos in food_set or (
                obstacles and pos in obstacles):
            continue
        food_type = random.randint(1, 3)
        food_set.add(SnakesFood(pos, food_type))
    return list(food_set)


def create_food(snake):
    """create_food: Создает один элемент еды в случайной позиции на поле."""

    while True:
        pos = (random.randint(0, Constants.FIELD_HEIGHT - 1),
               random.randint(0, Constants.FIELD_WIDTH - 1))
        if pos not in snake:
            food_type = random.randint(1, 2)
            return SnakesFood(pos, food_type)


"""SnakesFood: Класс, представляющий еду для змейки с разными типами."""


class SnakesFood:
    def __init__(self, position, food_type):
        """__init__: Инициализирует еду с позицией и типом (1-3)."""

        self.position = position
        self.food_type = food_type  # 1 или 2, или 3

    def get_char(self):
        """get_char: Возвращает символ еды в зависимости от типа."""

        if self.food_type == 1:
            return Constants.FOOD_CHAR1
        elif self.food_type == 2:
            return Constants.FOOD_CHAR2
        else:
            return Constants.FOOD_CHAR3

    def get_growth(self):
        """get_growth: Возвращает количество сегментов роста змейки от еды."""

        if self.food_type == 1:
            return 1
        elif self.food_type == 2:
            return 2
        else:
            return 3
