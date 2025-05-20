import unittest
from unittest.mock import patch, call, MagicMock, Mock

from logic.network import encode, decode_stream
from logic.obtacles_gen import generate_obstacles_mult, generate_obstacles
from logic.records import GameRecords


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
