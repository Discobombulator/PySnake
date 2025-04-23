import socket
import threading
import time
import random
from threading import Lock
from constants import Constants
from logic.obtacles_gen import generate_obstacles
from network import encode, decode


class GameServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.clients = {}
        self.snakes = {}
        self.directions = {}
        self.food_list = []
        self.obstacles = set()
        self.lock = Lock()
        self.running = False

    def init_player(self, player_id):
        with self.lock:
            # Инициализация змеи для игрока
            self.snakes[player_id] = {
                'body': [(random.randint(1, Constants.FIELD_HEIGHT - 2),
                          random.randint(1, Constants.FIELD_WIDTH - 2))],
                'direction': 'RIGHT'
            }
            self.directions[player_id] = 'RIGHT'

            # Генерация еды и препятствий только для первого игрока
            if len(self.snakes) == 1:
                self.generate_world()

    def generate_world(self):
        """Генерация еды и препятствий"""
        self.food_list = [(random.randint(1, Constants.FIELD_HEIGHT - 2)), (random.randint(1, Constants.FIELD_WIDTH - 2))]
        # Здесь можно добавить генерацию препятствий при необходимости

    def update_game(self):
        """Обновление игрового состояния"""
        with self.lock:
            # Движение змей
            for player_id, snake in self.snakes.items():
                direction = self.directions.get(player_id, 'RIGHT')
                head = snake['body'][0]

                # Вычисление новой позиции головы
                if direction == 'UP':
                    new_head = (head[0] - 1, head[1])
                elif direction == 'DOWN':
                    new_head = (head[0] + 1, head[1])
                elif direction == 'LEFT':
                    new_head = (head[0], head[1] - 1)
                else:  # RIGHT
                    new_head = (head[0], head[1] + 1)

                # Проверка столкновений
                if (new_head in self.obstacles or
                        any(new_head in s['body'] for pid, s in
                            self.snakes.items() if pid != player_id)):
                    self.reset_player(player_id)
                    continue

                snake['body'].insert(0, new_head)

                # Проверка еды
                if new_head == tuple(self.food_list):
                    self.food_list = [random.randint(1, Constants.FIELD_HEIGHT - 2),
                                      random.randint(1, Constants.FIELD_WIDTH - 2)]
                else:
                    snake['body'].pop()

    def reset_player(self, player_id):
        """Сброс позиции игрока"""
        with self.lock:
            self.snakes[player_id]['body'] = [
                (random.randint(1, Constants.FIELD_HEIGHT - 2),
                 random.randint(1, Constants.FIELD_WIDTH - 2))
            ]
            self.directions[player_id] = 'RIGHT'

    def handle_client(self, conn, addr, player_id):
        """Обработка подключения клиента"""
        print(f"Player {player_id} connected from {addr}")
        conn.send(encode({'id': player_id}))
        self.init_player(player_id)

        try:
            while True:
                data = decode(conn.recv(1024))
                if data and 'dir' in data:
                    with self.lock:
                        self.directions[player_id] = data['dir']
        except:
            print(f"Player {player_id} disconnected")
            with self.lock:
                self.snakes.pop(player_id, None)
                self.directions.pop(player_id, None)
            conn.close()

    def game_loop(self):
        """Основной игровой цикл"""
        while self.running:
            self.update_game()

            # Подготовка состояния для отправки
            state = {
                'snakes': {pid: s['body'] for pid, s in self.snakes.items()},
                'food': self.food_list,
                'size': (Constants.FIELD_HEIGHT, Constants.FIELD_WIDTH)
            }

            # Отправка состояния всем клиентам
            for player_id, conn in list(self.clients.items()):
                try:
                    personalized_state = state.copy()
                    personalized_state['your_id'] = player_id
                    conn.sendall(encode(personalized_state))
                except:
                    continue

            time.sleep(Constants.TICK_RATE)

    def start(self):
        """Запуск сервера"""
        self.running = True
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        # Запуск игрового цикла
        threading.Thread(target=self.game_loop, daemon=True).start()

        player_id = 1
        try:
            while self.running:
                conn, addr = self.socket.accept()
                self.clients[player_id] = conn
                threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr, player_id),
                    daemon=True
                ).start()
                player_id += 1
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Остановка сервера"""
        self.running = False
        self.socket.close()
        print("Server stopped")


if __name__ == '__main__':
    server = GameServer()
    server.start()