from constants import Constants


def draw_board(snake, food, std):
    std.clear()

    std.addstr(0, 0, Constants.BORDER_CHAR * (Constants.FIELD_WIDTH + 2))

    for row in range(Constants.FIELD_HEIGHT):
        line = Constants.BORDER_CHAR
        for col in range(Constants.FIELD_WIDTH):
            if (row, col) == food:
                line += Constants.FOOD_CHAR
            elif (row, col) in snake:
                line += Constants.SNAKE_CHAR
            else:
                line += ' '
        line += Constants.BORDER_CHAR
        std.addstr(row + 1, 0, line)

    std.addstr(Constants.FIELD_HEIGHT + 1, 0,
               Constants.BORDER_CHAR * (Constants.FIELD_WIDTH + 2))

    std.refresh()
