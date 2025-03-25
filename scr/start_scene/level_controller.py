from scr.game_scene.main_scene import start_game


def level_controller(std):
    key = std.getch()

    if key in [ord('1'), ord('!')]:
        return start_game(std, 1)
    elif key in [ord('2'), ord('@')]:
        return start_game(std, 2)
    elif key in [ord('3'), ord('#')]:
        return start_game(std, 3)
