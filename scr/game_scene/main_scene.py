import random
import time

from scr.constants import Constants
from scr.game_scene.game_controller import game_controller, check_end_game
from scr.game_scene.game_board import draw_board, generate_obstacles
from scr.game_scene.snakes_food import create_food
from scr.game_scene.snake import Snake
from scr.start_scene.records import GameRecords


def start_game(std, level):
    records = GameRecords()
    std.nodelay(True)
    std.timeout(100)

    initial_position = (Constants.FIELD_HEIGHT // 2, Constants.FIELD_WIDTH // 2)
    snake = Snake(initial_position, Constants.RIGHT)

    food = create_food(snake.body)
    i = random.randint(1, 2)
    obstacles = generate_obstacles(snake, food, level)
    horizontal_delay = 0.1
    vertical_delay = 0.1 * Constants.SPEED_RATIO

    while True:
        draw_board(snake, food, std, i, level=level, obstacles=obstacles)

        make_step = game_controller(snake.direction, std)
        if make_step == "brake":
            records.set_data(snake.get_length())
            break
        snake.update_direction(make_step)

        next_head = snake.get_next_head()

        if check_end_game(next_head, std, snake, obstacles):
            records.set_data(snake.get_length())
            break

        if next_head == food.position:
            snake.move(grow=True)
            for _ in range(
                    food.get_growth() - 1):  # уже вырос на 1, добавим остальное
                snake.move(grow=True)
            food = create_food(snake.body)
        else:
            snake.move(grow=False)

        # Разное время ожидания в зависимости от направления
        if snake.direction in [Constants.LEFT, Constants.RIGHT]:
            time.sleep(horizontal_delay)
        else:
            time.sleep(vertical_delay)
