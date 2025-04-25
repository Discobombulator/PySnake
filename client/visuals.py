import curses

from constants import Constants
from game_controller import check_end_game


def get_viewport_centered_on(head):
    row, col = head
    half_height = Constants.VIEW_HEIGHT // 2
    half_width = Constants.VIEW_WIDTH // 2

    top = max(0, min(Constants.FIELD_HEIGHT - Constants.VIEW_HEIGHT,
                     row - half_height))
    left = max(0, min(Constants.FIELD_WIDTH - Constants.VIEW_WIDTH,
                      col - half_width))

    return top, left


def draw_board(state, std, player_id_str, current_direction):
    """Отрисовка игрового поля"""
    snakes = state.get('snakes', {})
    food_list = state.get('food', [])
    obstacles = set(state.get('obstacles', []))

    # Проверки безопасности
    if player_id_str not in snakes:
        std.addstr(0, 0,
                   f"Игрок {player_id_str} не найден в списке змей: {list(snakes.keys())}")
        return

    if not snakes[player_id_str]:
        std.addstr(0, 0, f"Змея игрока {player_id_str} пуста!")
        return

    # Получаем координаты головы змеи игрока
    head = snakes[player_id_str][0]  # Первый элемент - голова
    top, left = get_viewport_centered_on(head)

    # Установка цветов
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)  # Змея игрока
    curses.init_pair(2, curses.COLOR_RED, -1)  # Еда тип 1
    curses.init_pair(3, curses.COLOR_WHITE, -1)  # Границы и препятствия
    curses.init_pair(4, curses.COLOR_YELLOW, -1)  # Чужие змеи
    curses.init_pair(5, curses.COLOR_BLUE, -1)  # Еда тип 2
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)  # Еда тип 3

    # Отрисовка верхней границы
    border_line = Constants.BORDER_CHAR * (Constants.VIEW_WIDTH + 2)
    std.addstr(0, 0, border_line, curses.color_pair(3))

    # Отрисовка игрового поля
    for row_offset in range(Constants.VIEW_HEIGHT):
        row = top + row_offset
        std.addstr(row_offset + 1, 0, Constants.BORDER_CHAR,
                   curses.color_pair(3))

        for col_offset in range(Constants.VIEW_WIDTH):
            col = left + col_offset
            cell = (row, col)

            symbol = ' '
            color = 0

            # Проверка, является ли клетка частью змеи игрока
            my_snake = snakes[player_id_str]
            is_my_snake = False

            for i, part in enumerate(my_snake):
                part_pos = tuple(part) if isinstance(part, list) else part
                if cell == part_pos:
                    is_my_snake = True
                    symbol = '@' if i == 0 else Constants.SNAKE_CHAR
                    color = curses.color_pair(1)
                    break

            if not is_my_snake:
                # Проверка, является ли клетка частью других змей
                for pid, snake_body in snakes.items():
                    if pid != player_id_str:
                        for i, part in enumerate(snake_body):
                            part_pos = tuple(part) if isinstance(part,
                                                                 list) else part
                            if cell == part_pos:
                                symbol = '#' if i == 0 else Constants.SNAKE_CHAR
                                color = curses.color_pair(4)
                                break

            # Проверка еды - теперь обрабатываем список объектов еды
            for food_item in food_list:
                if isinstance(food_item,
                              dict) and 'position' in food_item and 'food_type' in food_item:
                    # Получаем позицию еды
                    pos = food_item['position']
                    food_type = food_item['food_type']

                    # Преобразуем в кортеж, если нужно
                    food_pos = tuple(pos) if isinstance(pos, list) else pos

                    if cell == food_pos:
                        # Выбираем символ еды в зависимости от типа
                        if food_type == 1:
                            symbol = Constants.FOOD_CHAR1
                            color = curses.color_pair(2)  # красный для типа 1
                        elif food_type == 2:
                            symbol = Constants.FOOD_CHAR2
                            color = curses.color_pair(5)  # синий для типа 2
                        else:  # тип 3
                            symbol = Constants.FOOD_CHAR3
                            color = curses.color_pair(
                                6)  # фиолетовый для типа 3
                        break

            # Проверка, является ли клетка препятствием
            if cell in obstacles:
                symbol = Constants.OBSTACLE_CHAR
                color = curses.color_pair(3)

            std.addstr(row_offset + 1, col_offset + 1, symbol, color)

        # Отрисовка правой границы
        std.addstr(row_offset + 1, Constants.VIEW_WIDTH + 1,
                   Constants.BORDER_CHAR, curses.color_pair(3))

    # Отрисовка нижней границы
    std.addstr(Constants.VIEW_HEIGHT + 1, 0, border_line,
               curses.color_pair(3))

    # Отображение статистики
    std.addstr(2, Constants.VIEW_WIDTH + 5, f"Игрок ID: {player_id_str}")
    std.addstr(4, Constants.VIEW_WIDTH + 5,
               f"Длина змеи: {len(snakes[player_id_str])}")
    std.addstr(6, Constants.VIEW_WIDTH + 5,
               f"Направление: {current_direction}")
    std.addstr(8, Constants.VIEW_WIDTH + 5, f"Всего змей: {len(snakes)}")
    std.addstr(10, Constants.VIEW_WIDTH + 5,
               f"Голова: {snakes[player_id_str][0]}")
    std.addstr(12, Constants.VIEW_WIDTH + 5,
               f"Количество еды: {len(food_list)}")

    # Добавляем легенду еды
    std.addstr(14, Constants.VIEW_WIDTH + 5, "Еда:")
    std.addstr(15, Constants.VIEW_WIDTH + 5,
               f"{Constants.FOOD_CHAR1} - 1 рост", curses.color_pair(2))
    std.addstr(16, Constants.VIEW_WIDTH + 5,
               f"{Constants.FOOD_CHAR2} - 2 рост", curses.color_pair(5))
    std.addstr(17, Constants.VIEW_WIDTH + 5,
               f"{Constants.FOOD_CHAR3} - 3 рост", curses.color_pair(6))