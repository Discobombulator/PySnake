import socket
import threading
import time
import random
from threading import Lock
from constants import Constants
from controller.game_controller import check_end_game_mult
from logic.snakes_food import SnakesFood
from logic.network import encode
from logic.obtacles_gen import generate_obstacles_mult


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
            for player_id, snake in list(self.snakes.items()):
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

                # Проверка условий гибели змеи
                if check_end_game_mult(new_head, player_id, self.snakes,
                                       self.obstacles,
                                       Constants.FIELD_HEIGHT,
                                       Constants.FIELD_WIDTH):
                    # Отправляем сообщение о завершении игры клиенту
                    try:
                        client_conn = self.clients.get(player_id)
                        if client_conn:
                            client_conn.sendall(encode(
                                {'game_over': True, 'reason': 'collision'}))
                    except Exception as e:
                        print(
                            f"Failed to send game over message to player"
                            f" {player_id}: {e}")

                    # Удаляем игрока
                    if player_id in self.snakes:
                        del self.snakes[player_id]
                    if player_id in self.directions:
                        del self.directions[player_id]
                    if player_id in self.clients:
                        try:
                            self.clients[player_id].close()
                        except:
                            pass
                        del self.clients[player_id]

                    continue

                snake['body'].insert(0, new_head)

                # Проверка еды
                ate_food = False
                for i, food in enumerate(self.food_list):
                    if new_head == food.position:
                        # Увеличиваем змею в зависимости от типа еды
                        growth = food.get_growth() - 1
                        for _ in range(growth):
                            snake['body'].append(snake['body'][-1])

                        # Удаляем съеденную еду
                        self.food_list.pop(i)

                        # Создаем новую еду на безопасной позиции
                        new_food_pos = self.get_safe_position()
                        self.food_list.append(
                            SnakesFood(new_food_pos,
                                       random.randint(1, 3)))

                        ate_food = True
                        break

                # Удаляем хвост, если еда не была съедена
                if not ate_food:
                    snake['body'].pop()

    def handle_client(self, conn, addr, player_id):
        """Обработка подключения клиента"""
        print(f"Player {player_id} connected from {addr}")
        conn.sendall(encode({'id': player_id}))
        self.init_player(player_id)

        buffer = b""
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                buffer += data

                # Извлекаем полные сообщения
                from logic.network import decode_stream
                messages, buffer = decode_stream(buffer)

                for decoded_data in messages:
                    if decoded_data and 'dir' in decoded_data:
                        with self.lock:
                            current_dir = self.directions.get(player_id,
                                                              'RIGHT')
                            new_dir = decoded_data['dir']

                            invalid_turns = {
                                'UP': 'DOWN',
                                'DOWN': 'UP',
                                'LEFT': 'RIGHT',
                                'RIGHT': 'LEFT'
                            }

                            if new_dir != invalid_turns.get(current_dir):
                                self.directions[player_id] = new_dir
        except Exception as e:
            print(f"Player {player_id} disconnected: {e}")
        finally:
            with self.lock:
                self.snakes.pop(player_id, None)
                self.directions.pop(player_id, None)
            conn.close()

    def game_loop(self):
        """Основной игровой цикл"""
        while self.running:
            start_time = time.time()

            self.update_game()

            # Подготовка состояния для отправки
            # Преобразуем объекты еды в словари для сериализации
            food_data = [
                {'position': food.position, 'food_type': food.food_type}
                for food in self.food_list]

            state = {
                'snakes': {pid: s['body'] for pid, s in self.snakes.items()},
                'food': food_data,
                'obstacles': list(self.obstacles),
                # Преобразуем множество в список
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

            # Более точная задержка для поддержания желаемой частоты обновления
            elapsed = time.time() - start_time
            sleep_time = max(0, Constants.TICK_RATE - elapsed)
            time.sleep(sleep_time)

    def generate_world(self):
        """Генерация еды и препятствий"""
        # Создаем начальную еду
        self.food_list = []
        for _ in range(800):
            # При первоначальной генерации еды змей ещё нет,
            # поэтому проверяем только на пересечение с другой едой
            while True:
                pos = (random.randint(1, Constants.FIELD_HEIGHT - 2),
                       random.randint(1, Constants.FIELD_WIDTH - 2))

                if not any(pos == food.position for food in self.food_list):
                    break

            food_type = random.randint(1, 3)
            self.food_list.append(SnakesFood(pos, food_type))

        # Генерация препятствий (от 300 до 400)
        obstacle_count = random.randint(2000, 5000)
        print(f"Generating {obstacle_count} obstacles...")
        self.obstacles = generate_obstacles_mult(self, obstacle_count)
        print(f"Generated {len(self.obstacles)} obstacles")

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
