from logic.game import start_game


def level_controller(std):
    """ Контроллер для выбора сложности"""

    while True:
        key = std.getch()
        if key in [ord('1'), ord('!')]:
            level = 1
        elif key in [ord('2'), ord('@')]:
            level = 2
        elif key in [ord('3'), ord('#')]:
            level = 3
        else:
            continue  # если не выбрали уровень — ждём

        while True:
            result = start_game(std, level)

            if result == "brake":
                return "brake"  # пользователь вышел
            elif result == "play":
                continue
