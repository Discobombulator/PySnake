import curses

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


def check_end_game(new_head, obstacles=None):
    if (new_head[0] == 0 or new_head[0] == Constants.FIELD_HEIGHT or
            new_head[1] == 0 or new_head[1] == Constants.FIELD_WIDTH):
        return "brake"

    if obstacles is not None and new_head in obstacles:
        return "brake"
