import random
from constants import Constants

def generate_obstacles_mult(self, count):
    """Генерация препятствий"""
    obstacles = set()
    attempts = 0
    max_attempts = count * 10  # Максимальное количество попыток для избежания бесконечного цикла

    while len(obstacles) < count and attempts < max_attempts:
        pos = (random.randint(1, Constants.FIELD_HEIGHT - 2),
               random.randint(1, Constants.FIELD_WIDTH - 2))

        # Проверка, что позиция не занята едой
        if not any(pos == food.position for food in self.food_list):
            # Проверка, что позиция не занята другими змеями
            if not any(pos in snake['body'] for snake in
                       self.snakes.values()):
                # Проверка, что позиция не уже выбрана как препятствие
                if pos not in obstacles:
                    obstacles.add(pos)

        attempts += 1

    return obstacles

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
