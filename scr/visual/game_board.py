from scr.constants import Constants


def draw_board(snake, food, std, i, level=1, obstacles=None, ):
    std.clear()
    std.addstr(0, 0, Constants.BORDER_CHAR * (Constants.FIELD_WIDTH + 2))

    for row in range(Constants.FIELD_HEIGHT):
        line = Constants.BORDER_CHAR
        for col in range(Constants.FIELD_WIDTH):
            cell = (row, col)
            if cell == food.position:
                line += food.get_char()
            elif cell in snake.body:
                line += Constants.SNAKE_CHAR
            elif level in [2, 3] and obstacles and cell in obstacles:
                line += Constants.BORDER_CHAR
            else:
                line += ' '
        line += Constants.BORDER_CHAR
        std.addstr(row + 1, 0, line)

    std.addstr(Constants.FIELD_HEIGHT + 1, 0,
               Constants.BORDER_CHAR * (Constants.FIELD_WIDTH + 2))
    std.refresh()
