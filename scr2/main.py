import curses
import argparse

from scr.visual.start_scene import start_work
from scr2.logic.game import start_game


def main(std):
    start_game(std, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Консольная игра 'Змейка' "
                                                 "на Python. Для игры "
                                                 "используйте стрелочки, "
                                                 "для выхода q ")
    args = parser.parse_args()

    curses.wrapper(main)
