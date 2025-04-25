from constants import Constants
import random


def create_food_set(snake_body, obstacles, count=800):
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


class SnakesFood:
    def __init__(self, position, food_type):
        self.position = position
        self.food_type = food_type  # 1 или 2, или 3

    def get_char(self):
        if self.food_type == 1:
            return Constants.FOOD_CHAR1
        elif self.food_type == 2:
            return Constants.FOOD_CHAR2
        else:
            return Constants.FOOD_CHAR3

    def get_growth(self):
        if self.food_type == 1:
            return 1
        elif self.food_type == 2:
            return 2
        else:
            return 3
