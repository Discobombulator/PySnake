import curses
import argparse

from scr.start_scene.start_scene import start_work


def main(std):
    start_work(std)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Консольная игра 'Змейка' "
                                                 "на Python. Для игры "
                                                 "используйте стрелочки, "
                                                 "для выхода q ")
    args = parser.parse_args()

    curses.wrapper(main)
