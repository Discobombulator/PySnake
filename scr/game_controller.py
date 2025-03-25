import curses
import time

from scr.constants import Constants


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

def print_end(std,snake):
    std.clear()
    std.addstr(0, 0, "Вы проиграли(((")
    std.addstr(1, 0, "Вы ударились о границу!")
    std.addstr(2, 0, "Через 3 секунды игра закончится")
    std.addstr(3, 0, "Текущий трай - " + str(snake.get_length()))
    std.refresh()
    time.sleep(3)

def check_end_game(new_head, std, snake, obstacles=None):

    if (new_head[0] == 0 or new_head[0] == Constants.FIELD_HEIGHT - 1 or
        new_head[1] == 0 or new_head[1] == Constants.FIELD_WIDTH - 1):
        print_end(std, snake)
        return True

    if obstacles is not None and new_head in obstacles:
        print_end(std,snake)
        return True

    return False