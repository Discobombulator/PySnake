import json
import socket
import unittest
from unittest.mock import Mock, patch

from client import SnakeClient
from constants import Constants
from logic.network import encode, decode_stream, decode_single


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

        encoded_data = encode({'id': 1})
        client.sock.recv.side_effect = [encoded_data, Exception()]

        client.recv_loop()
        self.assertEqual(client.player_id, 1)
        self.assertEqual(client.player_id_str, '1')

    @patch('socket.socket')
    def test_recv_loop_your_id_received(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        encoded_data = encode({'your_id': 2})
        client.sock.recv.side_effect = [encoded_data, Exception()]

        client.recv_loop()
        self.assertEqual(client.player_id, 2)
        self.assertEqual(client.player_id_str, '2')

    @patch('socket.socket')
    def test_recv_loop_snakes_state(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        state_data = {'snakes': {'1': {'body': [[5, 5]]}}, 'food': []}
        encoded_data = encode(state_data)
        client.sock.recv.side_effect = [encoded_data, Exception()]

        client.recv_loop()
        self.assertEqual(client.state, state_data)

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

    @patch('socket.socket')
    def test_start_connection_error(self, mock_socket):
        client = SnakeClient()
        mock_std = Mock()

        mock_socket_instance = Mock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect.side_effect = socket.error(
            "Connection refused")

        with patch('curses.curs_set'), patch('time.sleep'):
            client.start(mock_std)

        mock_std.addstr.assert_called_with(0, 0,
                                           "Ошибка подключения: "
                                           "Connection refused")
        mock_std.refresh.assert_called()

    @patch('socket.socket')
    def test_recv_loop_multiple_messages(self, mock_socket):
        client = SnakeClient()
        client.sock = Mock()

        msg1 = {'id': 5}
        msg2 = {'snakes': {'5': {'body': [(10, 10)]}}, 'food': []}
        encoded_data = encode(msg1) + encode(msg2)

        client.sock.recv.side_effect = [encoded_data, Exception()]

        client.recv_loop()

        self.assertEqual(client.player_id, 5)
        self.assertEqual(client.player_id_str, '5')

    @patch('socket.socket')
    def test_decode_stream_functionality(self, mock_socket):
        msg1 = {'command': 'start'}
        msg2 = {'command': 'move'}

        encoded1 = json.dumps(msg1).encode(
            'utf-8') + Constants.MESSAGE_DELIMITER
        encoded2 = json.dumps(msg2).encode(
            'utf-8') + Constants.MESSAGE_DELIMITER

        incomplete = b'{"command": "stop'

        buffer = encoded1 + encoded2 + incomplete

        messages, remainder = decode_stream(buffer)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], msg1)
        self.assertEqual(messages[1], msg2)
        self.assertEqual(remainder, incomplete)

    @patch('socket.socket')
    @patch('threading.Thread')
    def test_client_key_handling(self, mock_thread, mock_socket):
        client = SnakeClient()
        client.sock = Mock()
        client.player_id_str = "1"
        mock_std = Mock()

        mock_std.getch.side_effect = [
            ord('w'),
            ord('a'),
            ord('s'),
            ord('d'),
            ord('q'),
        ]

        client.game_over = False

        def set_game_over():
            keys_processed = 0

            def side_effect(*args, **kwargs):
                nonlocal keys_processed
                keys_processed += 1
                if keys_processed >= 5:
                    client.game_over = True

            return side_effect

        mock_std.refresh.side_effect = set_game_over()

        with patch('curses.curs_set'), patch('time.sleep'):
            client.start(mock_std)

        expected_calls = [
            encode({'dir': 'UP'}),
            encode({'dir': 'LEFT'}),
            encode({'dir': 'DOWN'}),
            encode({'dir': 'RIGHT'}),
        ]

        self.assertEqual(client.sock.sendall.call_count, 4)

        for i, expected_call in enumerate(expected_calls):
            actual_call = client.sock.sendall.call_args_list[i][0][0]
            actual_decoded = decode_single(
                actual_call.split(Constants.MESSAGE_DELIMITER)[0])
            expected_decoded = decode_single(
                expected_call.split(Constants.MESSAGE_DELIMITER)[0])
            self.assertEqual(actual_decoded, expected_decoded)
