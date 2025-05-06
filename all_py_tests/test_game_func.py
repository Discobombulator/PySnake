import unittest
from unittest.mock import Mock, patch, MagicMock, call
import curses

from constants import Constants
from controller.game_controller import check_end_game_mult, game_controller
from logic.obtacles_gen import generate_obstacles_mult, generate_obstacles
from logic.records import GameRecords
from logic.snake import Snake
from logic.snakes_food import create_food_set, create_food, SnakesFood

from server import GameServer
from client import SnakeClient
from logic.network import encode, decode_stream


class TestGameController(unittest.TestCase):

    def test_game_controller(self):
        std = Mock()

        direction = Constants.RIGHT

        std.getch.return_value = curses.KEY_DOWN
        direction = game_controller(direction, std)
        self.assertEqual(direction, Constants.DOWN)

        std.getch.return_value = ord('q')
        self.assertEqual(game_controller(direction, std), "brake")

    def test_check_end_game_mult(self):
        new_head = (5, 5)
        player_id = 1
        snakes = {
            1: {'body': [(6, 5), (7, 5)]},
            2: {'body': [(5, 6), (5, 7)]}
        }
        obstacles = {(10, 10)}
        field_height = 20
        field_width = 20

        self.assertFalse(
            check_end_game_mult(new_head, player_id, snakes, obstacles,
                                field_height, field_width))

        self.assertTrue(
            check_end_game_mult((-1, 5), player_id, snakes, obstacles,
                                field_height, field_width))

        self.assertTrue(
            check_end_game_mult((10, 10), player_id, snakes, obstacles,
                                field_height, field_width))

        snakes[1]['body'] = [(6, 5), (5, 5)]
        self.assertTrue(
            check_end_game_mult((5, 5), player_id, snakes, obstacles,
                                field_height, field_width))

        snakes[2]['body'] = [(5, 5), (5, 6)]
        self.assertTrue(
            check_end_game_mult((5, 5), player_id, snakes, obstacles,
                                field_height, field_width))


class TestObstaclesGen(unittest.TestCase):
    def test_generate_obstacles_mult(self):
        server = MagicMock()
        server.food_list = [Mock(position=(1, 1))]
        server.snakes = {'player1': {'body': [(3, 3)]}}

        obstacles = generate_obstacles_mult(server, 10)
        self.assertIsInstance(obstacles, set)

    def test_generate_obstacles(self):
        snake = Mock()
        snake.body = [(5, 5)]
        food = (10, 10)

        obstacles = generate_obstacles(snake, food, 1)
        self.assertEqual(len(obstacles), 0)

        with patch('random.randint', return_value=5000):
            with patch('random.sample', return_value=[(1, 1), (2, 2)]):
                obstacles = generate_obstacles(snake, food, 2)
                self.assertEqual(len(obstacles), 2)

        with patch('random.randint', return_value=10000):
            with patch('random.sample', return_value=[(3, 3), (4, 4),
                                                      (5, 6)]):
                obstacles = generate_obstacles(snake, food, 3)
                self.assertEqual(len(obstacles), 3)


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


class TestGameRecords(unittest.TestCase):
    @patch('builtins.open', new_callable=unittest.mock.mock_open,
           read_data="10\n5\n3\n")
    def test_init_and_load_data(self, mock_file):
        records = GameRecords()
        self.assertEqual(records._data, [10, 5, 3])
        mock_file.assert_called_once_with("rec.txt", "r")

    def test_get_data(self):
        records = GameRecords()
        records._data = [10, 5, 3]
        self.assertEqual(records.get_data(), [10, 5, 3])

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_set_data(self, mock_file):
        records = GameRecords()
        records._data = [10, 5, 3]
        records.set_data(15)
        self.assertEqual(records._data, [15, 10, 5])

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_data(self, mock_file):
        with patch.object(GameRecords, '__init__', return_value=None):
            records = GameRecords()
            records._data = [10, 5, 3]

            records.save_data()

            mock_file.assert_called_once_with("rec.txt", "w")
            handle = mock_file()
            self.assertEqual(handle.write.call_count, 3)
            handle.write.assert_has_calls([
                call("10\n"), call("5\n"), call("3\n")
            ])

    @patch('builtins.open')
    def test_load_data_file_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError()
        records = GameRecords()
        self.assertEqual(records._data, [0, 0, 0])


class TestSnakeClient(unittest.TestCase):
    @patch('socket.socket')
    def test_init(self, mock_socket):
        client = SnakeClient()
        self.assertEqual(client.server_ip, 'localhost')
        self.assertEqual(client.port, 12345)

    @patch('socket.socket')
    def test_recv_loop(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        encoded_data = encode({'id': 1})
        client.sock.recv.side_effect = [encoded_data, Exception()]

        client.recv_loop()
        self.assertEqual(client.player_id, 1)

    @patch('socket.socket')
    def test_recv_loop_game_over(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        encoded_data = encode({'game_over': True})
        client.sock.recv.side_effect = [encoded_data]

        client.recv_loop()
        self.assertTrue(client.game_over)


# Tests for server.py
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


class TestNetwork(unittest.TestCase):
    def test_encode(self):
        data = {'test': 'value'}
        encoded = encode(data)
        self.assertTrue(isinstance(encoded, bytes))
        self.assertIn(b'test', encoded)
        self.assertIn(b'value', encoded)

    def test_decode_stream(self):
        data1 = {'test1': 'value1'}
        data2 = {'test2': 'value2'}

        encoded1 = encode(data1)
        encoded2 = encode(data2)

        buffer = encoded1 + encoded2[:-2]

        messages, remaining = decode_stream(buffer)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], data1)
        self.assertEqual(remaining, encoded2[:-2])


if __name__ == '__main__':
    unittest.main()
