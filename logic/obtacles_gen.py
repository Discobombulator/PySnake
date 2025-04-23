import random
from constants import Constants


def generate_obstacles(snake, food):
    total_cells = [(row, col) for row in range(Constants.FIELD_HEIGHT)
                   for col in range(Constants.FIELD_WIDTH)]

    # Исправленная проверка для snake и food
    available = total_cells.copy()
    if snake is not None:
        available = [cell for cell in available if cell not in snake.body]
    if food is not None:
        available = [cell for cell in available if cell != food]

    num_obstacles = random.randint(5000, 10000)

    # Защита от случая, когда доступных клеток меньше, чем нужно препятствий
    num_obstacles = min(num_obstacles, len(available))
    return set(random.sample(available, num_obstacles))
