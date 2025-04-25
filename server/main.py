import socket
import threading
import time
import random
from threading import Lock
from constants import Constants
from logic.obtacles_gen import generate_obstacles
from logic.snakes_food import create_food_set, SnakesFood
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

    def get_safe_position(self):
        """Получение безопасного положения для спавна змеи"""
        while True:
            pos = (random.randint(1, Constants.FIELD_HEIGHT - 2),
                   random.randint(1, Constants.FIELD_WIDTH - 2))

            # Проверка, что позиция не занята едой
            if not any(pos == food.position for food in self.food_list):
                # Проверка, что позиция не занята другими змеями
                if not any(pos in snake['body'] for snake in
                           self.snakes.values()):
                    # Проверка, что позиция не занята препятствиями
                    if pos not in self.obstacles:
                        return pos

    def init_player(self, player_id):
        with self.lock:
            # Инициализация змеи для игрока с безопасной позицией
            safe_pos = self.get_safe_position()
            self.snakes[player_id] = {
                'body': [safe_pos],
                'direction': 'RIGHT'
            }
            self.directions[player_id] = 'RIGHT'

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
                ate_food = False
                for i, food in enumerate(self.food_list):
                    if new_head == food.position:
                        # Увеличиваем змею в зависимости от типа еды
                        growth = food.get_growth() - 1  # -1 потому что одно звено уже добавлено
                        for _ in range(growth):
                            snake['body'].append(snake['body'][-1])

                        # Удаляем съеденную еду
                        self.food_list.pop(i)

                        # Создаем новую еду на безопасной позиции
                        new_food_pos = self.get_safe_position()
                        self.food_list.append(
                            SnakesFood(new_food_pos, random.randint(1, 3)))

                        ate_food = True
                        break

                # Удаляем хвост, если еда не была съедена
                if not ate_food:
                    snake['body'].pop()

    def reset_player(self, player_id):
        """Сброс позиции игрока"""
        with self.lock:
            safe_pos = self.get_safe_position()
            self.snakes[player_id]['body'] = [safe_pos]
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
            # Преобразуем объекты еды в словари для сериализации
            food_data = [
                {'position': food.position, 'food_type': food.food_type}
                for food in self.food_list]

            state = {
                'snakes': {pid: s['body'] for pid, s in self.snakes.items()},
                'food': food_data,
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

    def generate_world(self):
        """Генерация еды и препятствий"""
        # Создаем начальную еду (10 единиц еды)
        self.food_list = []
        for _ in range(189):
            while True:
                pos = (random.randint(1, Constants.FIELD_HEIGHT - 2),
                       random.randint(1, Constants.FIELD_WIDTH - 2))

                # Проверяем, что новая позиция не совпадает с уже существующей едой
                if not any(pos == food.position for food in self.food_list):
                    break

            food_type = random.randint(1, 3)
            self.food_list.append(SnakesFood(pos, food_type))

        # Здесь можно добавить генерацию препятствий при необходимости
        # self.obstacles = generate_obstacles(None, None)

    def start(self):
        """Запуск сервера"""
        self.running = True
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        self.generate_world()

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