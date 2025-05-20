import unittest
from unittest.mock import Mock, patch


class TestPlayingController(unittest.TestCase):
    def setUp(self):
        from controller.end_game_controller import playing_controller
        self.playing_controller = playing_controller
        self.std_mock = Mock()

    @patch('curses.KEY_ENTER', 10)  # Устанавливаем значение KEY_ENTER
    def test_playing_controller_enter_key(self):
        self.std_mock.getch.side_effect = [10]  # Клавиша Enter

        result = self.playing_controller(self.std_mock)

        self.assertEqual(result, "play")
        self.std_mock.getch.assert_called_once()

    def test_playing_controller_curses_enter_key(self):
        with patch('curses.KEY_ENTER', 343):
            self.std_mock.getch.side_effect = [
                343]  # Симулируем нажатие KEY_ENTER

            result = self.playing_controller(self.std_mock)

            self.assertEqual(result, "play")
            self.std_mock.getch.assert_called_once()

    def test_playing_controller_q_key(self):
        self.std_mock.getch.side_effect = [ord('q')]

        # Вызываем тестируемую функцию
        result = self.playing_controller(self.std_mock)

        # Проверяем, что функция возвращает "brake"
        self.assertEqual(result, "brake")
        # Проверяем, что метод getch был вызван
        self.std_mock.getch.assert_called_once()

    def test_playing_controller_cyrillic_q_key(self):
        self.std_mock.getch.side_effect = [ord('й')]

        # Вызываем тестируемую функцию
        result = self.playing_controller(self.std_mock)

        # Проверяем, что функция возвращает "brake"
        self.assertEqual(result, "brake")
        # Проверяем, что метод getch был вызван
        self.std_mock.getch.assert_called_once()

    def test_playing_controller_other_keys(self):
        self.std_mock.getch.side_effect = [ord('a'), ord('b'), ord('c'),
                                           10]  # Разные клавиши, затем Enter

        # Вызываем тестируемую функцию
        result = self.playing_controller(self.std_mock)

        # Проверяем, что функция возвращает "play"
        self.assertEqual(result, "play")
        # Проверяем, что метод getch был вызван 4 раза
        self.assertEqual(self.std_mock.getch.call_count, 4)


if __name__ == '__main__':
    unittest.main()