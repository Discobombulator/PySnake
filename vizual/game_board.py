import curses

from constants import Constants


def get_viewport_centered_on(head):
    row, col = head
    half_height = Constants.VIEW_HEIGHT // 2
    half_width = Constants.VIEW_WIDTH // 2

    top = max(0, min(Constants.FIELD_HEIGHT - Constants.VIEW_HEIGHT,
                     row - half_height))
    left = max(0, min(Constants.FIELD_WIDTH - Constants.VIEW_WIDTH,
                      col - half_width))

    return top, left


def init_colors():
    # Убедимся, что терминал поддерживает цвета
    curses.start_color()
    if curses.has_colors():
        curses.start_color()

        # Определение цветовых пар
        curses.init_pair(1, curses.COLOR_GREEN,
                         curses.COLOR_BLACK)  # Змея
        curses.init_pair(2, curses.COLOR_RED,
                         curses.COLOR_BLACK)  # Еда +1
        curses.init_pair(3, curses.COLOR_CYAN,
                         curses.COLOR_BLACK)  # Еда +2
        curses.init_pair(4, curses.COLOR_MAGENTA,
                         curses.COLOR_BLACK)  # Еда +3
        curses.init_pair(5, curses.COLOR_BLUE,
                         curses.COLOR_BLACK)  # Препятствия
        curses.init_pair(6, curses.COLOR_WHITE,
                         curses.COLOR_BLACK)  # Границы и текст
        curses.init_pair(7, curses.COLOR_YELLOW,
                         curses.COLOR_BLACK)  # Голова змеи


def draw_board(snake, food_list, std, level=1, obstacles=None):
    std.clear()

    head = snake.body[0]
    top, left = get_viewport_centered_on(head)

    # Отрисовка верхней границы
    border_line = Constants.BORDER_CHAR * (Constants.VIEW_WIDTH + 2)
    std.addstr(0, 0, border_line, curses.color_pair(6))

    for row_offset in range(Constants.VIEW_HEIGHT):
        row = top + row_offset
        # Левая граница
        std.addch(row_offset + 1, 0, Constants.BORDER_CHAR,
                  curses.color_pair(6))

        for col_offset in range(Constants.VIEW_WIDTH):
            col = left + col_offset
            cell = (row, col)

            symbol = ' '
            color_pair = 0  # Дефолтный цвет

            if any(food.position == cell for food in food_list):
                food = next(f for f in food_list if f.position == cell)
                symbol = food.get_char()
                # Определение цвета в зависимости от типа еды
                if food.get_growth() == 1:
                    color_pair = 2  # Красный для еды +1
                elif food.get_growth() == 2:
                    color_pair = 3  # Голубой для еды +2
                elif food.get_growth() == 3:
                    color_pair = 4  # Пурпурный для еды +3
            elif cell == snake.body[0]:  # Голова змеи
                symbol = Constants.SNAKE_CHAR
                color_pair = 7  # Желтый для головы змеи
            elif cell in snake.body:  # Тело змеи
                symbol = Constants.SNAKE_CHAR
                color_pair = 1  # Зеленый для тела змеи
            elif level in [2, 3] and obstacles and cell in obstacles:
                symbol = Constants.OBSTACLE_CHAR
                color_pair = 5  # Синий для препятствий

            # Отрисовка символа с нужным цветом
            std.addch(row_offset + 1, col_offset + 1, symbol,
                      curses.color_pair(color_pair))

        # Правая граница
        std.addch(row_offset + 1, Constants.VIEW_WIDTH + 1,
                  Constants.BORDER_CHAR, curses.color_pair(6))

    # Отрисовка нижней границы
    std.addstr(Constants.VIEW_HEIGHT + 1, 0, border_line, curses.color_pair(6))

    # Отрисовка информации справа от игрового поля
    info_col = Constants.VIEW_WIDTH + 3

    std.addstr(4, info_col, f"Длина змеи: {snake.get_length()}",
               curses.color_pair(6))
    std.addstr(6, info_col, f"Направление: {snake.direction}",
               curses.color_pair(6))
    std.addstr(8, info_col, f"Голова: {head}", curses.color_pair(6))

    # Добавляем легенду еды
    std.addstr(16, Constants.VIEW_WIDTH + 5, "Легенда:")
    std.addstr(17, Constants.VIEW_WIDTH + 5,
               f"{Constants.FOOD_CHAR1} - еда +1", curses.color_pair(2))
    std.addstr(18, Constants.VIEW_WIDTH + 5,
               f"{Constants.FOOD_CHAR2} - еда +2", curses.color_pair(5))
    std.addstr(19, Constants.VIEW_WIDTH + 5,
               f"{Constants.FOOD_CHAR3} - еда +3", curses.color_pair(6))

    std.refresh()
