from controller.end_game_controller import playing_controller


def print_end(std, snake):
    std.clear()
    std.addstr(0, 0, "Вы проиграли(((")
    std.addstr(1, 0, "Вы ударились о границу!")
    std.addstr(3, 0, "Текущий трай - " + str(snake.get_length()))
    std.addstr(4, 0, "Выйти - [q]")
    std.addstr(5, 0, "Перезапустить - [Enter]")
    std.addstr(6, 0, "Введите: ")

    if playing_controller(std) == "play":
        std.clear()  # Сброс экрана перед новым запуском
        return "play"
    else:
        std.clear()  # Сброс экрана перед новым запуском
        return "brake"
