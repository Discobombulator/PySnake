import curses

from constants import Constants
from vizual.end_scene import print_end


def check_end_game_mult(new_head, player_id, snakes, obstacles,
                        field_height, field_width):
    # Проверка столкновения со стеной
    if (new_head[0] < 0 or new_head[0] >= field_height or
            new_head[1] < 0 or new_head[1] >= field_width):
        return True

    # Проверка столкновения с препятствием
    if new_head in obstacles:
        return True

    # Проверка столкновения с телом своей змеи
    if player_id in snakes:
        snake = snakes[player_id]
        # Проверяем со 2-й позиции, т.к. голова сейчас в new_head
        if new_head in snake['body'][1:]:
            return True

    # Проверка столкновения с другими змеями
    for pid, snake in snakes.items():
        if pid != player_id:  # Не проверяем столкновение с самим собой
            if new_head in snake['body']:
                return True

    return False


def game_controller(direction, std):
    key = std.getch()

    if key == curses.KEY_UP and direction != Constants.DOWN:
        return Constants.UP
    elif key == curses.KEY_DOWN and direction != Constants.UP:
        return Constants.DOWN
    elif key == curses.KEY_LEFT and direction != Constants.RIGHT:
        return Constants.LEFT
    elif key == curses.KEY_RIGHT and direction != Constants.LEFT:
        return Constants.RIGHT
    elif key in [ord('q'), ord('й')]:
        return "brake"

    return direction


def check_end_game(new_head, std, snake, obstacles=None):
    if (new_head[0] == 0 or new_head[0] == Constants.FIELD_HEIGHT or
            new_head[1] == 0 or new_head[1] == Constants.FIELD_WIDTH):
        if print_end(std, snake) == "play":
            return "restart"
        else:
            return "brake"

    if obstacles is not None and new_head in obstacles:
        if print_end(std, snake) == "play":
            return "restart"
        else:
            return "brake"

    return None
