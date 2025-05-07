import curses
import unittest
from unittest.mock import Mock, patch, call

from client import SnakeClient
from logic.network import encode


class TestClient(unittest.TestCase):
    @patch('socket.socket')
    def test_init(self, mock_socket):
        client = SnakeClient()
        self.assertEqual(client.server_ip, 'localhost')
        self.assertEqual(client.port, 12345)
        self.assertEqual(client.state, {})
        self.assertIsNone(client.player_id)
        self.assertIsNone(client.player_id_str)
        self.assertEqual(client.direction, 'RIGHT')
        self.assertIsNone(client.sock)
        self.assertFalse(client.game_over)
        self.assertEqual(client.buffer, b"")

    @patch('socket.socket')
    def test_recv_loop_id_received(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        # Test receiving player ID
        encoded_data = encode({'id': 1})
        client.sock.recv.side_effect = [encoded_data, Exception()]

        client.recv_loop()
        self.assertEqual(client.player_id, 1)
        self.assertEqual(client.player_id_str, '1')

    @patch('socket.socket')
    def test_recv_loop_your_id_received(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        # Test receiving your_id format
        encoded_data = encode({'your_id': 2})
        client.sock.recv.side_effect = [encoded_data, Exception()]

        client.recv_loop()
        self.assertEqual(client.player_id, 2)
        self.assertEqual(client.player_id_str, '2')

    @patch('socket.socket')
    def test_recv_loop_snakes_state(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        state_data = {'snakes': {'1': {'body': [(5, 5)]}}, 'food': []}
        encoded_data = encode(state_data)
        client.sock.recv.side_effect = [encoded_data, Exception()]

        client.recv_loop()
        self.assertEqual({'food': [], 'snakes': {'1': {'body': [(5, 5)]}}}, state_data)

    @patch('socket.socket')
    def test_recv_loop_connection_lost(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()
        client.sock.recv.return_value = b""

        client.recv_loop()
        self.assertTrue(client.game_over)

    @patch('socket.socket')
    def test_recv_loop_game_over(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        encoded_data = encode({'game_over': True})
        client.sock.recv.side_effect = [encoded_data]

        client.recv_loop()
        self.assertTrue(client.game_over)
