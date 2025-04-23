import curses

from constants import Constants
from network import encode, KEYS


def game_controller(direction, self, std):
    key = std.getch()


    if key in [ord('q'), ord('й')]:
        return "brake"
    if key in KEYS:
        new_dir = KEYS[key]
        if new_dir != direction:
            direction = new_dir
    return direction





def check_end_game(new_head, obstacles=None):
    if (new_head[0] == 0 or new_head[0] == Constants.FIELD_HEIGHT or
            new_head[1] == 0 or new_head[1] == Constants.FIELD_WIDTH):
        return "brake"

    if obstacles is not None and new_head in obstacles:
        return "brake"
