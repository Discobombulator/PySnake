import random

from scr.constants import Constants


def generate_obstacles(snake, food, level):
    total_cells = [(row, col) for row in range(Constants.FIELD_HEIGHT)
                   for col in range(Constants.FIELD_WIDTH)]
    available = [cell for cell in total_cells if cell not in snake.body
                 and cell != food]
    if level == 2:
        num_obstacles = random.randint(10, 30)
        return set(random.sample(available, num_obstacles))
    elif level == 3:
        num_obstacles = random.randint(60, 100)
        return set(random.sample(available, num_obstacles))

    else:
        return []
