import curses
import time
import argparse

from constants import Constants
from game_board import draw_board
from game_controller import controller, check_end_game
from snakes_food import create_food


def main(std):
    std.nodelay(True)
    std.timeout(100)

    snake = [(Constants.FIELD_HEIGHT // 2, Constants.FIELD_WIDTH // 2)]
    direction = Constants.RIGHT
    food = create_food(snake)

    while True:
        draw_board(snake, food, std)

        make_step = controller(direction, std)
        if make_step == "brake":
            break
        direction = make_step

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if check_end_game(new_head, std, snake):
            break

        snake.insert(0, new_head)

        if new_head == food:
            food = create_food(snake)
        else:
            snake.pop()

        time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Консольная игра 'Змейка' "
                                                 "на Python. Для игры "
                                                 "используйте стрелочки, "
                                                 "для выхода q ")
    args = parser.parse_args()

    curses.wrapper(main)
