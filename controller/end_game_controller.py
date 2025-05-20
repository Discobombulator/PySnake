import curses


def playing_controller(std):
    """ Контроллер для рестарта игры"""
    while True:
        key = std.getch()

        if key in [10, curses.KEY_ENTER]:
            return "play"
        elif key in [ord('q'), ord('й')]:
            return "brake"
