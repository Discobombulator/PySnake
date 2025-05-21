import unittest
from unittest.mock import patch, Mock

from constants import Constants
from controller.game_controller import check_end_game_mult
from logic.network import encode
from logic.snakes_food import SnakesFood
from server import GameServer


class TestGameServer(unittest.TestCase):
    def test_init(self):
        server = GameServer(host='127.0.0.1', port=12345)
        self.assertEqual(server.host, '127.0.0.1')
        self.assertEqual(server.port, 12345)

    def test_get_safe_position(self):
        server = GameServer()
        server.food_list = [Mock(position=(5, 5))]
        server.snakes = {'player1': {'body': [(10, 10)]}}
        server.obstacles = {(15, 15)}

        pos = server.get_safe_position()
        self.assertNotIn(pos, [food.position for food in server.food_list])
        self.assertNotIn(pos, [(10, 10)])
        self.assertNotIn(pos, server.obstacles)

    def test_init_player(self):
        server = GameServer()
        server.food_list = []
        server.snakes = {}
        server.obstacles = set()
        server.directions = {}

        with patch.object(server, 'get_safe_position', return_value=(5, 5)):
            server.init_player(1)
            self.assertIn(1, server.snakes)
            self.assertEqual(server.snakes[1]['body'], [(5, 5)])
            self.assertEqual(server.directions[1], 'RIGHT')

    def test_update_game(self):
        server = GameServer()
        server.food_list = [SnakesFood((5, 6), 1)]
        server.snakes = {1: {'body': [(5, 5)]}}
        server.directions = {1: 'RIGHT'}
        server.obstacles = set()
        server.clients = {1: Mock()}

        server.update_game()
        self.assertEqual(server.snakes[1]['body'], [(5, 6), (5, 5)])

    @patch('socket.socket')
    def test_stop(self, mock_socket):
        server = GameServer()
        server.running = True
        server.socket = Mock()

        server.stop()
        self.assertFalse(server.running)
        server.socket.close.assert_called_once()

    @patch('socket.socket')
    def test_handle_client(self, mock_socket):
        server = GameServer()
        server.clients = {}
        server.snakes = {}
        server.directions = {}

        conn = Mock()
        encoded_data = encode({'dir': 'UP'})
        conn.recv.side_effect = [encoded_data, b""]

        with patch.object(server, 'init_player'):
            server.handle_client(conn, ('127.0.0.1', 12345), 1)
            conn.sendall.assert_called_once()

    def test_check_end_game_mult_method(self):
        GameServer()

        new_head = (-1, 5)
        player_id = 1
        snakes = {1: {'body': [(0, 5)]}}
        obstacles = set()

        result = check_end_game_mult(
            new_head, player_id, snakes, obstacles,
            Constants.FIELD_HEIGHT, Constants.FIELD_WIDTH
        )
        self.assertTrue(result)

        new_head = (5, 5)
        obstacles = {(5, 5)}

        result = check_end_game_mult(
            new_head, player_id, snakes, obstacles,
            Constants.FIELD_HEIGHT, Constants.FIELD_WIDTH
        )
        self.assertTrue(result)

        new_head = (5, 5)
        obstacles = set()

        result = check_end_game_mult(
            new_head, player_id, snakes, obstacles,
            Constants.FIELD_HEIGHT, Constants.FIELD_WIDTH
        )
        self.assertFalse(result)

    def test_generate_world(self):
        server = GameServer()
        server.generate_world()

        self.assertEqual(len(server.food_list), 400)

        self.assertGreater(len(server.obstacles), 0)

        for food in server.food_list:
            self.assertIsInstance(food, SnakesFood)
            self.assertTrue(1 <= food.food_type <= 3)
            self.assertIsInstance(food.position, tuple)
            self.assertEqual(len(food.position), 2)

    @patch('socket.socket')
    def test_update_game_eating_food(self, mock_socket):
        server = GameServer()

        player_id = 1
        food_pos = (5, 6)
        snake_head = (5, 5)
        server.food_list = [SnakesFood(food_pos, 2)]
        server.snakes = {player_id: {'body': [snake_head]}}
        server.directions = {player_id: 'RIGHT'}
        server.obstacles = set()
        server.clients = {player_id: Mock()}

        server.update_game()

        self.assertEqual(len(server.snakes[player_id]['body']), 3)
        self.assertEqual(server.snakes[player_id]['body'][0], food_pos)

        self.assertEqual(len(server.food_list), 1)
        self.assertNotEqual(server.food_list[0].position, food_pos)

    @patch('socket.socket')
    def test_handle_client_direction_change(self, mock_socket):
        server = GameServer()
        server.clients = {}
        server.snakes = {}
        server.directions = {}

        player_id = 1
        server.directions[player_id] = 'RIGHT'

        conn = Mock()
        encoded_data = encode({'dir': 'UP'})
        conn.recv.side_effect = [encoded_data, b""]

        with patch.object(server, 'init_player'):
            server.handle_client(conn, ('127.0.0.1', 12345), player_id)

            self.assertEqual(server.directions.get(player_id), None)

    @patch('socket.socket')
    def test_handle_client_invalid_direction_change(self, mock_socket):
        server = GameServer()
        server.clients = {}
        server.snakes = {}
        server.directions = {}

        player_id = 1
        server.directions[player_id] = 'UP'

        conn = Mock()
        encoded_data = encode({'dir': 'DOWN'})
        conn.recv.side_effect = [encoded_data, b""]

        with patch.object(server, 'init_player'):
            server.handle_client(conn, ('127.0.0.1', 12345), player_id)

            self.assertEqual(server.directions.get(player_id), None)

    @patch('socket.socket')
    @patch('threading.Thread')
    def test_start_server(self, mock_thread, mock_socket):
        server = GameServer()

        mock_socket_instance = Mock()
        mock_socket.return_value = mock_socket_instance

        mock_socket_instance.accept.side_effect = [
            (Mock(), ('127.0.0.1', 54321)),
            KeyboardInterrupt
        ]

        with patch.object(server, 'generate_world'):
            server.start()

            self.assertFalse(server.running)
            mock_socket_instance.bind.assert_called_once_with(
                ('0.0.0.0', 12345))
            mock_socket_instance.listen.assert_called_once()

            mock_thread.assert_called()

            self.assertIn(1, server.clients)
            mock_thread.assert_called()
