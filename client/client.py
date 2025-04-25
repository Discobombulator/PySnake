import curses
import socket
import threading
import time

from client.clients_visual import draw_board
from network import encode, decode, KEYS


class SnakeClient:
    def __init__(self, server_ip='localhost', port=12345):
        self.server_ip = server_ip
        self.port = port
        self.state = {}
        self.player_id = None
        self.player_id_str = None  # Добавляем строковую версию ID
        self.direction = 'RIGHT'
        self.sock = None
        self.game_over = False

    def recv_loop(self):
        """Цикл приема данных от сервера"""
        while True:
            try:
                data = self.sock.recv(8192)
                if data:
                    decoded_data = decode(data)

                    if 'id' in decoded_data:
                        self.player_id = decoded_data['id']
                        self.player_id_str = str(
                            self.player_id)  # Сохраняем строковую версию

                    if 'your_id' in decoded_data:
                        self.player_id = decoded_data['your_id']
                        self.player_id_str = str(
                            self.player_id)  # Сохраняем строковую версию

                    # Проверка на сообщение о завершении игры
                    if 'game_over' in decoded_data and decoded_data[
                        'game_over']:
                        reason = decoded_data.get('reason', 'unknown')
                        print(f"\nИгра окончена: {reason}")
                        # Закрываем соединение
                        self.sock.close()
                        # Устанавливаем флаг завершения игры
                        self.game_over = True
                        break

                    if 'snakes' in decoded_data:
                        self.state = decoded_data

            except Exception as e:
                print(f"Ошибка приема данных: {e}")
                break

    def start(self, std):
        """Запуск клиента"""
        std.timeout(100)

        self.sock = socket.socket()
        try:
            self.sock.connect((self.server_ip, self.port))
        except Exception as e:
            std.addstr(0, 0, f"Ошибка подключения: {e}")
            std.refresh()
            time.sleep(3)
            return

        # Запуск потока для приема данных
        recv_thread = threading.Thread(target=self.recv_loop, daemon=True)
        recv_thread.start()

        curses.curs_set(0)
        std.nodelay(True)
        std.timeout(100)

        time.time()
        frame_count = 0

        while not self.game_over:  # Проверяем флаг завершения игры
            frame_count += 1

            # Обработка ввода
            try:
                key = std.getch()
                if key != -1:
                    if key in KEYS:
                        new_dir = KEYS[key]
                        if new_dir != self.direction:
                            self.direction = new_dir
                            self.sock.send(encode({'dir': new_dir}))
                    elif key in [ord('q'), ord('й')]:
                        break
            except Exception as e:
                std.addstr(0, 0, f"Ошибка ввода: {e}")
                std.refresh()
                break

            # Отрисовка игры
            try:
                std.clear()
                draw_board(self.state, std, self.player_id_str, self.direction)
            except Exception as e:
                std.addstr(0, 0, f"Ошибка отрисовки: {str(e)}")
                std.refresh()

        # Если игра завершена, показываем сообщение
        if self.game_over:
            std.clear()
            std.refresh()
            std.getch()  # Ждем нажатия клавиши

        try:
            self.sock.close()
        except:
            pass


if __name__ == '__main__':
    client = SnakeClient()
    curses.wrapper(client.start)
