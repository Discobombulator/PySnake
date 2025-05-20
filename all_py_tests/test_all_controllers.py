import curses
import unittest
from unittest.mock import Mock

from constants import Constants
from controller.game_controller import game_controller


class TestGameController(unittest.TestCase):
    def test_game_controller_up(self):
        std = Mock()
        std.getch.return_value = curses.KEY_UP
        direction = Constants.RIGHT

        result = game_controller(direction, std)
        self.assertEqual(result, Constants.UP)

    def test_game_controller_down(self):
        std = Mock()
        std.getch.return_value = curses.KEY_DOWN
        direction = Constants.RIGHT

        result = game_controller(direction, std)
        self.assertEqual(result, Constants.DOWN)

    def test_game_controller_left(self):
        std = Mock()
        std.getch.return_value = curses.KEY_LEFT
        direction = Constants.UP

        result = game_controller(direction, std)
        self.assertEqual(result, Constants.LEFT)

    def test_game_controller_right(self):
        std = Mock()
        std.getch.return_value = curses.KEY_RIGHT
        direction = Constants.UP

        result = game_controller(direction, std)
        self.assertEqual(result, Constants.RIGHT)

    def test_game_controller_invalid_direction(self):
        std = Mock()
        std.getch.return_value = curses.KEY_UP
        direction = Constants.DOWN

        result = game_controller(direction, std)
        self.assertEqual(result, Constants.DOWN)  # Should not change direction

    def test_game_controller_quit(self):
        std = Mock()
        std.getch.return_value = ord('q')
        direction = Constants.RIGHT

        result = game_controller(direction, std)
        self.assertEqual(result, "brake")

    def test_game_controller_quit_russian(self):
        std = Mock()
        std.getch.return_value = ord('й')
        direction = Constants.RIGHT

        result = game_controller(direction, std)
        self.assertEqual(result, "brake")

    def test_game_controller_no_key(self):
        std = Mock()
        std.getch.return_value = -1  # No key pressed
        direction = Constants.RIGHT

        result = game_controller(direction, std)
        self.assertEqual(result,
                         Constants.RIGHT)  # Direction should not change
