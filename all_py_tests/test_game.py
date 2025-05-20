import unittest
from unittest.mock import MagicMock, patch
import sys
import os
from logic.game import start_game
from constants import Constants

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGame(unittest.TestCase):
    @patch('logic.game.init_colors')
    @patch('logic.game.draw_board')
    @patch('logic.game.generate_obstacles')
    @patch('logic.game.create_food_set')
    @patch('logic.game.game_controller')
    @patch('logic.game.check_end_game')
    @patch('time.sleep')
    @patch('curses.curs_set')
    def test_start_game_setup(self, mock_curs_set,
                              mock_check_end_game,
                              mock_game_controller, mock_create_food_set,
                              mock_generate_obstacles, mock_draw_board,
                              mock_init_colors):
        mock_std = MagicMock()
        mock_check_end_game.return_value = None
        mock_game_controller.return_value = Constants.RIGHT

        food_mock = MagicMock()
        food_mock.position = (10, 10)
        food_mock.get_growth.return_value = 1
        mock_create_food_set.return_value = [food_mock]

        mock_generate_obstacles.return_value = []

        mock_game_controller.side_effect = [Constants.RIGHT, Constants.RIGHT,
                                            "brake"]

        result = start_game(mock_std, 1)

        mock_init_colors.assert_called_once()
        mock_std.nodelay.assert_called_once_with(True)
        mock_std.timeout.assert_called_once_with(100)
        mock_curs_set.assert_called_once_with(0)
        mock_generate_obstacles.assert_called_once()
        mock_create_food_set.assert_called_once()

        self.assertEqual(mock_draw_board.call_count >= 1, True)
        self.assertEqual(mock_game_controller.call_count, 3)

        self.assertEqual(result, None)

    @patch('logic.game.init_colors')
    @patch('logic.game.draw_board')
    @patch('logic.game.generate_obstacles')
    @patch('logic.game.create_food_set')
    @patch('logic.game.game_controller')
    @patch('logic.game.check_end_game')
    @patch('time.sleep')
    @patch('curses.curs_set')
    def test_snake_movement(self, mock_curs_set, mock_sleep,
                            mock_check_end_game,
                            mock_game_controller, mock_create_food_set,
                            mock_generate_obstacles, mock_draw_board,
                            mock_init_colors):
        mock_std = MagicMock()
        mock_check_end_game.return_value = None

        food_mock = MagicMock()
        food_mock.position = (
            100, 100)
        food_mock.get_growth.return_value = 1
        mock_create_food_set.return_value = [food_mock]

        mock_generate_obstacles.return_value = []

        mock_game_controller.side_effect = [Constants.RIGHT, Constants.RIGHT,
                                            "brake"]

        result = start_game(mock_std, 1)

        self.assertEqual(result, None)

        self.assertEqual(mock_game_controller.call_count, 3)

    @patch('logic.game.init_colors')
    @patch('logic.game.draw_board')
    @patch('logic.game.generate_obstacles')
    @patch('logic.game.create_food_set')
    @patch('logic.game.game_controller')
    @patch('logic.game.check_end_game')
    @patch('time.sleep')
    @patch('curses.curs_set')
    def test_food_eating(self, mock_curs_set, mock_sleep, mock_check_end_game,
                         mock_game_controller, mock_create_food_set,
                         mock_generate_obstacles, mock_draw_board,
                         mock_init_colors):
        mock_std = MagicMock()
        mock_check_end_game.return_value = None

        food_mock = MagicMock()
        food_mock.position = (Constants.FIELD_HEIGHT // 2,
                              Constants.FIELD_WIDTH // 2 + 1)
        food_mock.get_growth.return_value = 1
        mock_create_food_set.side_effect = [[food_mock], [
            MagicMock()]]

        mock_generate_obstacles.return_value = []

        mock_game_controller.side_effect = [Constants.RIGHT, "brake"]

        result = start_game(mock_std, 1)

        self.assertEqual(result, None)

        self.assertEqual(mock_create_food_set.call_count, 2)

    @patch('logic.game.init_colors')
    @patch('logic.game.draw_board')
    @patch('logic.game.generate_obstacles')
    @patch('logic.game.create_food_set')
    @patch('logic.game.game_controller')
    @patch('logic.game.check_end_game')
    @patch('logic.game.GameRecords')
    @patch('time.sleep')
    @patch('curses.curs_set')
    def test_game_over(self, mock_curs_set, mock_sleep, mock_records,
                       mock_check_end_game,
                       mock_game_controller, mock_create_food_set,
                       mock_generate_obstacles, mock_draw_board,
                       mock_init_colors):
        mock_std = MagicMock()

        records_instance = MagicMock()
        mock_records.return_value = records_instance

        food_mock = MagicMock()
        food_mock.position = (100, 100)
        food_mock.get_growth.return_value = 1
        mock_create_food_set.return_value = [food_mock]

        mock_generate_obstacles.return_value = []

        mock_game_controller.return_value = Constants.RIGHT
        mock_check_end_game.side_effect = [None, "brake"]

        result = start_game(mock_std, 1)

        self.assertEqual(result, "brake")

        records_instance.set_data.assert_called_once()

    @patch('logic.game.init_colors')
    @patch('logic.game.draw_board')
    @patch('logic.game.generate_obstacles')
    @patch('logic.game.create_food_set')
    @patch('logic.game.game_controller')
    @patch('logic.game.check_end_game')
    @patch('logic.game.GameRecords')
    @patch('time.sleep')
    @patch('curses.curs_set')
    def test_restart_game(self, mock_curs_set, mock_sleep, mock_records,
                          mock_check_end_game,
                          mock_game_controller, mock_create_food_set,
                          mock_generate_obstacles, mock_draw_board,
                          mock_init_colors):
        mock_std = MagicMock()

        records_instance = MagicMock()
        mock_records.return_value = records_instance

        food_mock = MagicMock()
        food_mock.position = (100, 100)
        food_mock.get_growth.return_value = 1
        mock_create_food_set.return_value = [food_mock]

        mock_generate_obstacles.return_value = []

        mock_game_controller.return_value = Constants.RIGHT
        mock_check_end_game.return_value = "restart"

        result = start_game(mock_std, 1)

        self.assertEqual(result, "play")

        records_instance.set_data.assert_not_called()


if __name__ == '__main__':
    unittest.main()
