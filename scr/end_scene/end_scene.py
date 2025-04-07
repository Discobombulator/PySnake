import curses
import time


def playing_controller(std):
    while True:
        key = std.getch()

        if key in [10, curses.KEY_ENTER]:
            return "play"
        elif key in [ord('q'), ord('й')]:
            return "brake"


def print_end(std, snake):

    std.clear()
    std.addstr(0, 0, "Вы проиграли(((")
    std.addstr(1, 0, "Вы ударились о границу!")
    std.addstr(3, 0, "Текущий трай - " + str(snake.get_length()))
    std.refresh()
    std.addstr(4, 0, "Выйти - [q]")
    std.addstr(5, 0, "Перезапустить - [Enter]")
    std.addstr(6, 0, "Введите: ")


    if playing_controller(std) == "play":
        std.clear()  # Сброс экрана перед новым запуском
        return "play"
    else:
        std.clear()  # Сброс экрана перед новым запуском
        return "brake"