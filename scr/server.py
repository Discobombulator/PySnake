import socket
import threading
import json
import time

from logic.obtacles_gen import generate_obstacles
from logic.snake import Snake
from logic.snakes_food import create_food_set

TICK_RATE = 0.1
PORT = 12345
HOST = '0.0.0.0'

clients = []
players = {}
food = []
obstacles = set()


class GameState:
    def __init__(self):
        self.snakes = {}
        self.food = []
        self.obstacles = set()
        self.level = 1

    def to_dict(self):
        return {
            "snakes": {pid: snake.body for pid, snake in self.snakes.items()},
            "food": [f.position for f in self.food],
            "obstacles": list(self.obstacles),
            "level": self.level
        }


def handle_client(conn, addr, player_id):
    print(f"[+] Подключён клиент {addr}, игрок {player_id}")
    players[player_id] = Snake((15, player_id * 10 + 5), (0, 1))

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            direction = json.loads(data.decode())
            players[player_id].update_direction(tuple(direction))
    except:
        pass

    print(f"[-] Клиент {player_id} отключился")
    del players[player_id]
    conn.close()


def game_loop():
    global food, obstacles
    game_state = GameState()

    # Инициализация еды и препятствий
    food = create_food_set([], obstacles, count=50)
    obstacles = generate_obstacles(Snake((0, 0), (0, 1)), None,
                                   game_state.level)

    while True:
        start_time = time.time()

        # Обновление состояния
        game_state.food = food
        game_state.obstacles = obstacles
        game_state.snakes = players

        # Движение змеек
        for pid, snake in players.items():
            next_head = snake.get_next_head()

            # Проверка коллизий
            if (next_head in obstacles or
                    any(next_head in s.body for s in players.values() if
                        s != snake)):
                del players[pid]
                continue

            snake.move(grow=False)

            # Проверка съедения еды
            for f in food:
                if f.position == snake.body[0]:
                    snake.move(grow=True)
                    food.remove(f)
                    food.extend(
                        create_food_set(snake.body, obstacles, count=1))

        # Рассылка состояния
        state_data = json.dumps(game_state.to_dict()).encode()
        for conn in clients:
            try:
                conn.sendall(state_data)
            except:
                clients.remove(conn)

        # Контроль частоты обновления
        elapsed = time.time() - start_time
        time.sleep(max(0, TICK_RATE - elapsed))


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Сервер слушает на {HOST}:{PORT}")

    threading.Thread(target=game_loop, daemon=True).start()

    player_id = 0
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr, player_id),
                         daemon=True).start()
        player_id += 1


if __name__ == "__main__":
    start_server()