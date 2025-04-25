import curses
import socket
import threading
import time

from vizual.clients_visual import draw_board_mult
from logic.network import encode, decode_stream


class SnakeClient:
    def __init__(self, server_ip='localhost', port=12345):
        self.server_ip = server_ip
        self.port = port
        self.state = {}
        self.player_id = None
        self.player_id_str = None
        self.direction = 'RIGHT'
        self.sock = None
        self.game_over = False
        self.buffer = b""  # Буфер для приема данных

    def recv_loop(self):
        """Цикл приема данных от сервера"""
        while not self.game_over:
            try:
                data = self.sock.recv(32768)  # Увеличиваем размер буфера
                if not data:
                    print("Соединение с сервером потеряно")
                    self.game_over = True
                    break

                # Добавляем данные в буфер
                self.buffer += data

                # Извлекаем полные сообщения
                messages, self.buffer = decode_stream(self.buffer)

                for decoded_data in messages:
                    if 'id' in decoded_data:
                        self.player_id = decoded_data['id']
                        self.player_id_str = str(self.player_id)

                    if 'your_id' in decoded_data:
                        self.player_id = decoded_data['your_id']
                        self.player_id_str = str(self.player_id)

                    if 'game_over' in decoded_data and decoded_data[
                        'game_over']:
                        self.game_over = True
                        break

                    if 'snakes' in decoded_data:
                        self.state = decoded_data

            except Exception as e:
                print(f"Ошибка приема данных: {e}")
                self.game_over = True
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

        while not self.game_over:
            current_time = time.time()
            frame_count += 1

            # Обработка ввода
            try:
                key = std.getch()
                if key != -1:
                    from logic.network import KEYS
                    if key in KEYS:
                        new_dir = KEYS[key]
                        if new_dir != self.direction:
                            self.direction = new_dir
                            self.sock.sendall(encode({'dir': new_dir}))
                    elif key in [ord('q'), ord('й')]:
                        break
            except Exception as e:
                std.addstr(0, 0, f"Ошибка ввода: {e}")
                std.refresh()
                break

            # Отрисовка игры
            try:
                if self.player_id_str:  # Проверяем, что ID получен
                    std.clear()
                    draw_board_mult(self.state, std, self.player_id_str,
                                    self.direction)
                else:
                    std.clear()
                    std.addstr(0, 0, "Ожидание ID от сервера...")
                    std.refresh()
            except Exception as e:
                std.clear()
                std.addstr(0, 0, f"Ошибка отрисовки: {str(e)}")
                std.refresh()

            # Контроль частоты кадров
            frame_time = time.time() - current_time
            if frame_time < 0.05:  # Не более 20 FPS
                time.sleep(0.05 - frame_time)

        # Если игра завершена, показываем сообщение
        if self.game_over:
            std.clear()

        try:
            self.sock.close()
        except:
            pass


if __name__ == '__main__':
    client = SnakeClient()
    curses.wrapper(client.start)
