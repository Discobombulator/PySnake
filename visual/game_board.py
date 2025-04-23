import curses

from constants import Constants

def get_viewport_centered_on(head):
    row, col = head
    half_height = Constants.VIEW_HEIGHT // 2
    half_width = Constants.VIEW_WIDTH // 2

    top = max(0, min(Constants.FIELD_HEIGHT - Constants.VIEW_HEIGHT, row - half_height))
    left = max(0, min(Constants.FIELD_WIDTH - Constants.VIEW_WIDTH, col - half_width))

    return top, left

def draw_board(snake, food_list, std, level=1, obstacles=None):
    std.clear()

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)

    head = snake.body[0]
    top, left = get_viewport_centered_on(head)

    border_line = Constants.BORDER_CHAR * (Constants.VIEW_WIDTH + 2)
    std.addstr(0, 0, border_line)

    for row_offset in range(Constants.VIEW_HEIGHT):
        row = top + row_offset
        for col_offset in range(Constants.VIEW_WIDTH):
            col = left + col_offset
            cell = (row, col)

            symbol = ' '
            color = 0  # Нет цвета по умолчанию

            food = None

            for f in food_list:
                if f.position == cell:
                    food = f
                    break

            if food is not None:
                symbol = food.get_char()
                color = curses.color_pair(1)

            elif cell in snake.body:
                symbol = Constants.SNAKE_CHAR

            elif level in [2, 3] and obstacles and cell in obstacles:
                symbol = Constants.OBSTACLE_CHAR

            std.addstr(row_offset + 1, col_offset + 1, symbol, color)

        # Границы слева и справа
        std.addstr(row_offset + 1, 0, Constants.BORDER_CHAR)
        std.addstr(row_offset + 1, Constants.VIEW_WIDTH + 1,
                   Constants.BORDER_CHAR)

    # Верх и низ
    border_line = Constants.BORDER_CHAR * (Constants.VIEW_WIDTH + 2)
    std.addstr(0, 0, border_line)
    std.addstr(Constants.VIEW_HEIGHT + 1, 0, border_line)

    std.refresh()

