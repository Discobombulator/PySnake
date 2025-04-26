import curses
import argparse

from vizual.start_scene import start_work


def main(std):
    while True:
        result = start_work(std)
        if result == "brake":
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Консольная игра 'Змейка' "
                                                 "на Python. Для игры "
                                                 "используйте стрелочки, "
                                                 "для выхода q ")
    args = parser.parse_args()

    curses.wrapper(main)
