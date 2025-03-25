import unittest
import curses

from unittest.mock import MagicMock
from scr.constants import Constants
from scr.game_scene.snakes_food import create_food
from scr.game_scene.game_controller import game_controller, check_end_game


class TestGameFunctions(unittest.TestCase):

    def test_create_food(self):
        snake = [(5, 5), (5, 6), (5, 7)]

        for _ in range(5):
            food = create_food(snake)
            self.assertNotIn(food, snake)
            self.assertTrue(0 <= food[0] < Constants.FIELD_HEIGHT)
            self.assertTrue(0 <= food[1] < Constants.FIELD_WIDTH)

    def test_controller(self):
        stdscr = MagicMock()

        stdscr.getch.return_value = curses.KEY_UP
        self.assertEqual(game_controller(Constants.RIGHT, stdscr), Constants.UP)

        stdscr.getch.return_value = ord('q')
        self.assertEqual(game_controller(Constants.RIGHT, stdscr),
                         "brake")  # Проверка выхода

    def test_check_end_game(self):
        stdscr = MagicMock()
        snake = [(5, 5), (5, 6), (5, 7)]

        self.assertTrue(check_end_game((5, Constants.FIELD_WIDTH),
                                       stdscr, []))
        self.assertTrue(check_end_game((5, 6), stdscr, snake))


if __name__ == "__main__":
    unittest.main()
