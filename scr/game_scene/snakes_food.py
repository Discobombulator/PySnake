from scr.constants import Constants
import random


def create_food(snake):
    while True:
        pos = (random.randint(0, Constants.FIELD_HEIGHT - 1),
               random.randint(0, Constants.FIELD_WIDTH - 1))
        if pos not in snake:
            food_type = random.randint(1, 2)
            return SnakesFood(pos, food_type)


class SnakesFood:
    def __init__(self, position, food_type):
        self.position = position
        self.food_type = food_type  # 1 или 2

    def get_char(self):
        if self.food_type == 1:
            return Constants.FOOD_CHAR1
        else:
            return Constants.FOOD_CHAR2

    def get_growth(self):
        return 1 if self.food_type == 1 else 3
