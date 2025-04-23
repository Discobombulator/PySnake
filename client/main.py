import curses
import socket
import threading
import time

from client.visuals import draw_board
from constants import Constants
from game_controller import game_controller, check_end_game
from logic import snake
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

                    if 'snakes' in decoded_data:
                        self.state = decoded_data


            except Exception as e:
                break

    def start(self, std):
        """Запуск клиента"""
        std.timeout(100)

        self.sock = socket.socket()
        try:
            self.sock.connect((self.server_ip, self.port))
        except Exception as e:
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

        while True:

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
                break

            # Отрисовка игры
            try:
                std.clear()

                draw_board(self.state, std, self.player_id_str,
                               self.direction)

            except Exception as e:
                std.addstr(0, 0, f"Ошибка отрисовки: {str(e)}")
                std.refresh()

            if self.direction in [Constants.LEFT, Constants.RIGHT]:
                time.sleep(0.1)
            else:
                time.sleep(0.3) # Задержка для снижения нагрузки на CPU

        self.sock.close()

if __name__ == '__main__':
    client = SnakeClient()
    curses.wrapper(client.start)