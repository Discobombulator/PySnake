from Constants import Constants
import random


def create_food(snake):

    while True:
        pos = (random.randint(0, Constants.FIELD_HEIGHT - 1),
               random.randint(0, Constants.FIELD_WIDTH - 1))
        if pos not in snake:
            return pos


class SnakesFood:
    def __init__(self, snake):
        self.snake = snake
