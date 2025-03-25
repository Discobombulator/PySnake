import random

from scr.constants import Constants


def draw_board(snake, food, std,i , level=1, obstacles=None, ):
    std.clear()

    std.addstr(0, 0, Constants.BORDER_CHAR * (Constants.FIELD_WIDTH + 2))

    for row in range(Constants.FIELD_HEIGHT):
        line = Constants.BORDER_CHAR
        for col in range(Constants.FIELD_WIDTH):
            cell = (row, col)
            if cell == food:

                if i ==1:
                    line += Constants.FOOD_CHAR1
                else:
                    line += Constants.FOOD_CHAR2
            elif cell in snake.body:
                line += Constants.SNAKE_CHAR
            elif level in [2, 3] and obstacles and cell in obstacles:
                line += Constants.BORDER_CHAR  # например, "#"
            else:
                line += ' '
        line += Constants.BORDER_CHAR
        std.addstr(row + 1, 0, line)

    std.addstr(Constants.FIELD_HEIGHT + 1, 0, Constants.BORDER_CHAR * (Constants.FIELD_WIDTH + 2))
    std.refresh()


def generate_obstacles(snake, food, level):
    total_cells = [(row, col) for row in range(Constants.FIELD_HEIGHT)
                   for col in range(Constants.FIELD_WIDTH)]
    available = [cell for cell in total_cells if cell not in snake.body and cell != food]
    if level == 2:
        num_obstacles = random.randint(10, 30)
        return set(random.sample(available, num_obstacles))
    elif level == 3:
        num_obstacles = random.randint(60, 100)
        return set(random.sample(available, num_obstacles))

    else:
        return []
