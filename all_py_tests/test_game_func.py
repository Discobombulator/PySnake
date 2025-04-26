import unittest
import curses

from unittest.mock import MagicMock

from constants import Constants
from controller.game_controller import game_controller


class TestGameFunctions(unittest.TestCase):

    def test_controller(self):
        stdscr = MagicMock()

        stdscr.getch.return_value = curses.KEY_UP
        self.assertEqual(game_controller(Constants.RIGHT, stdscr),
                         Constants.UP)

        stdscr.getch.return_value = ord('q')
        self.assertEqual(game_controller(Constants.RIGHT, stdscr),
                         "brake")  # Проверка выхода


if __name__ == "__main__":
    unittest.main()
