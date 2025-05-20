import unittest
from unittest.mock import patch

from constants import Constants
from logic.snake import Snake
from logic.snakes_food import create_food_set, create_food, SnakesFood


class TestSnake(unittest.TestCase):
    def test_init(self):
        snake = Snake((5, 5), (0, 1))
        self.assertEqual(snake.body, [(5, 5)])
        self.assertEqual(snake.direction, (0, 1))

    def test_update_direction(self):
        snake = Snake((5, 5), (0, 1))
        snake.update_direction((1, 0))
        self.assertEqual(snake.direction, (1, 0))

    def test_get_next_head(self):
        snake = Snake((5, 5), (0, 1))
        self.assertEqual(snake.get_next_head(), (5, 6))

    def test_move(self):
        snake = Snake((5, 5), (0, 1))
        snake.move(grow=False)
        self.assertEqual(snake.body, [(5, 6)])

    def test_move_with_growth(self):
        snake = Snake((5, 5), (0, 1))
        snake.move(grow=True)
        self.assertEqual(snake.body, [(5, 6), (5, 5)])

    def test_cut_tail(self):
        snake = Snake((5, 5), (0, 1))
        snake.body = [(5, 8), (5, 7), (5, 6), (5, 5)]
        snake.cut_tail((5, 6))
        self.assertEqual(snake.body, [(5, 8), (5, 7)])

    def test_get_length(self):
        snake = Snake((5, 5), (0, 1))
        self.assertEqual(snake.get_length(), 1)


class TestSnakesFood(unittest.TestCase):
    def test_create_food_set(self):
        snake_body = [(5, 5)]
        obstacles = {(10, 10)}

        with patch('random.randint', return_value=1):
            food_set = create_food_set(snake_body, obstacles, count=1)
            self.assertEqual(len(food_set), 1)

    def test_create_food(self):
        snake_body = [(5, 5)]

        with patch('random.randint', side_effect=[10, 10, 1]):
            food = create_food(snake_body)
            self.assertIsInstance(food, SnakesFood)

    def test_snakes_food_init(self):
        food = SnakesFood((5, 5), 1)
        self.assertEqual(food.position, (5, 5))
        self.assertEqual(food.food_type, 1)

    def test_get_char(self):
        food = SnakesFood((5, 5), 1)
        self.assertEqual(food.get_char(), Constants.FOOD_CHAR1)

        food = SnakesFood((5, 5), 2)
        self.assertEqual(food.get_char(), Constants.FOOD_CHAR2)

        food = SnakesFood((5, 5), 3)
        self.assertEqual(food.get_char(), Constants.FOOD_CHAR3)

    def test_get_growth(self):
        food = SnakesFood((5, 5), 1)
        self.assertEqual(food.get_growth(), 1)

        food = SnakesFood((5, 5), 2)
        self.assertEqual(food.get_growth(), 2)

        food = SnakesFood((5, 5), 3)
        self.assertEqual(food.get_growth(), 3)
