import time

from scr2.constants import Constants
from scr2.controllers.game_controller import game_controller, check_end_game
from scr2.logic.obtacles_gen import generate_obstacles
from scr2.visual.game_board import draw_board
from scr2.logic.snakes_food import create_food_set
from scr2.logic.snake import Snake


def start_game(std, level):
    std.nodelay(True)
    std.timeout(100)

    initial_position = (
        Constants.FIELD_HEIGHT // 2, Constants.FIELD_WIDTH // 2)
    snake = Snake(initial_position, Constants.RIGHT)

    obstacles = generate_obstacles(snake, None, level)
    food_list = create_food_set(snake.body, obstacles, count=1000)

    horizontal_delay = 0.1
    vertical_delay = 0.1 * Constants.SPEED_RATIO

    while True:
        draw_board(snake, food_list, std, level=level, obstacles=obstacles)

        make_step = game_controller(snake.direction, std)
        if make_step == "brake":
            break
        snake.update_direction(make_step)

        next_head = snake.get_next_head()
        game_status = check_end_game(next_head, obstacles)
        if game_status == "brake":
            return "brake"

        eaten = None
        for food in food_list:
            if next_head == food.position:
                eaten = food
                break

        if eaten:
            food_list.remove(eaten)
            for _ in range(eaten.get_growth()):
                snake.move(grow=True)
            new_food = create_food_set(snake.body, obstacles, count=1)
            food_list.extend(new_food)
        else:
            snake.move(grow=False)

        if snake.direction in [Constants.LEFT, Constants.RIGHT]:
            time.sleep(horizontal_delay)
        else:
            time.sleep(vertical_delay)
