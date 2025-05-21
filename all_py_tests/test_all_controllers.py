from controller.level_controller import level_controller
from controller.game_controller import game_controller
import unittest
from unittest.mock import MagicMock
import curses
import sys
import os
from unittest.mock import Mock, patch

from constants import Constants
from controller.game_controller import check_end_game
from logic.snake import Snake

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGameController(unittest.TestCase):

    def setUp(self):
        self.std_mock = Mock()
        initial_position = (10, 10)
        initial_direction = Constants.RIGHT
        self.snake = Snake(initial_position, initial_direction)

    @patch('controller.game_controller.print_end')
    def test_check_end_game_collision_with_wall_top(self, mock_print_end):
        mock_print_end.return_value = "play"

        new_head = (0, 10)
        result = check_end_game(new_head, self.std_mock, self.snake)

        self.assertEqual(result, "restart")
        mock_print_end.assert_called_once_with(self.std_mock, self.snake)

    @patch('controller.game_controller.print_end')
    def test_check_end_game_collision_with_wall_bottom(self, mock_print_end):
        mock_print_end.return_value = "play"

        new_head = (Constants.FIELD_HEIGHT, 10)
        result = check_end_game(new_head, self.std_mock, self.snake)

        self.assertEqual(result, "restart")
        mock_print_end.assert_called_once_with(self.std_mock, self.snake)

    @patch('controller.game_controller.print_end')
    def test_check_end_game_collision_with_wall_left(self, mock_print_end):
        mock_print_end.return_value = "play"

        new_head = (10, 0)
        result = check_end_game(new_head, self.std_mock, self.snake)

        self.assertEqual(result, "restart")
        mock_print_end.assert_called_once_with(self.std_mock, self.snake)

    def test_check_end_game_no_collision(self):
        new_head = (15, 15)
        obstacles = {(5, 5), (20, 20)}

        result = check_end_game(new_head, self.std_mock, self.snake, obstacles)

        self.assertIsNone(result)

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
                         Constants.RIGHT)


class TestLevelController(unittest.TestCase):
    @patch('controller.level_controller.start_game')
    def test_level_selection_key_1(self, mock_start_game):
        mock_std = MagicMock()

        mock_std.getch.side_effect = [ord('1'), ord('q')]

        mock_start_game.return_value = "brake"

        result = level_controller(mock_std)

        mock_start_game.assert_called_once_with(mock_std, 1)

        self.assertEqual(result, "brake")

    @patch('controller.level_controller.start_game')
    def test_level_selection_key_2(self, mock_start_game):
        mock_std = MagicMock()

        mock_std.getch.side_effect = [ord('2'), ord('q')]

        mock_start_game.return_value = "brake"

        result = level_controller(mock_std)

        mock_start_game.assert_called_once_with(mock_std, 2)

        self.assertEqual(result, "brake")

    @patch('controller.level_controller.start_game')
    def test_level_selection_key_3(self, mock_start_game):
        mock_std = MagicMock()

        mock_std.getch.side_effect = [ord('3'), ord('q')]

        mock_start_game.return_value = "brake"

        result = level_controller(mock_std)

        mock_start_game.assert_called_once_with(mock_std, 3)

        self.assertEqual(result, "brake")

    @patch('controller.level_controller.start_game')
    def test_ignores_invalid_keys(self, mock_start_game):
        mock_std = MagicMock()

        mock_std.getch.side_effect = [ord('x'), ord('1'), ord('q')]

        mock_start_game.return_value = "brake"

        result = level_controller(mock_std)

        mock_start_game.assert_called_once_with(mock_std, 1)

        self.assertEqual(result, "brake")

    @patch('controller.level_controller.start_game')
    def test_restart_game(self, mock_start_game):
        mock_std = MagicMock()

        mock_std.getch.side_effect = [ord('1')]

        mock_start_game.side_effect = ["play", "brake"]

        result = level_controller(mock_std)

        self.assertEqual(mock_start_game.call_count, 2)
        mock_start_game.assert_called_with(mock_std, 1)

        self.assertEqual(result, "brake")


if __name__ == '__main__':
    unittest.main()
