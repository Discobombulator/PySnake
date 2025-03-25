import random
import time

from scr.constants import Constants
from scr.game_controller import game_controller, check_end_game
from scr.game_scene.game_board import draw_board, generate_obstacles
from scr.game_scene.snakes_food import create_food
from scr.snake import Snake
from scr.start_scene.records import GameRecords


def start_game(std, level):
    records = GameRecords()
    std.nodelay(True)
    std.timeout(100)

    # Инициализируем змею: начальное положение — центр поля, направление вправо
    initial_position = (Constants.FIELD_HEIGHT // 2, Constants.FIELD_WIDTH // 2)
    snake = Snake(initial_position, Constants.RIGHT)

    # Создаем еду, передавая текущее положение змеи для избежания коллизии
    food = create_food(snake.body)
    i = random.randint(1, 2)
    obstacles = generate_obstacles(snake, food, level)
    while True:

        draw_board(snake, food, std,i, level=level, obstacles=obstacles)

        # Получаем новое направление из контроллера
        make_step = game_controller(snake.direction, std)
        if make_step == "brake":
            records.set_data(snake.get_length())
            break
        snake.update_direction(make_step)

        next_head = snake.get_next_head()

        # Проверка: не столкнулась ли змейка с препятствиями/себя самой
        if check_end_game(next_head, std, snake, obstacles):
            records.set_data(snake.get_length())
            break

        # Если следующая позиция совпадает с едой, двигаем змейку с ростом, иначе — обычное движение
        if next_head == food:
            snake.move(grow=True)
            i = random.randint(1, 2)
            food = create_food(snake.body)
        else:
            snake.move(grow=False)

        time.sleep(0.1)
