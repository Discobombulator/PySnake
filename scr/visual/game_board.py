from scr.constants import Constants

def get_viewport_centered_on(head):
    row, col = head
    half_height = Constants.VIEW_HEIGHT // 2
    half_width = Constants.VIEW_WIDTH // 2

    top = max(0, min(Constants.FIELD_HEIGHT - Constants.VIEW_HEIGHT, row - half_height))
    left = max(0, min(Constants.FIELD_WIDTH - Constants.VIEW_WIDTH, col - half_width))

    return top, left

def draw_board(snake, food_list, std, level=1, obstacles=None):
    std.clear()

    head = snake.body[0]
    top, left = get_viewport_centered_on(head)

    border_line = Constants.BORDER_CHAR * (Constants.VIEW_WIDTH + 2)
    std.addstr(0, 0, border_line)

    for row_offset in range(Constants.VIEW_HEIGHT):
        row = top + row_offset
        line = Constants.BORDER_CHAR
        for col_offset in range(Constants.VIEW_WIDTH):
            col = left + col_offset
            cell = (row, col)

            symbol = ' '
            if any(food.position == cell for food in food_list):
                food = next(f for f in food_list if f.position == cell)
                symbol = food.get_char()
            elif cell in snake.body:
                symbol = Constants.SNAKE_CHAR
            elif level in [2, 3] and obstacles and cell in obstacles:
                symbol = Constants.OBSTACLE_CHAR

            line += symbol
        line += Constants.BORDER_CHAR
        std.addstr(row_offset + 1, 0, line)

    std.addstr(Constants.VIEW_HEIGHT + 1, 0, border_line)
    std.refresh()

