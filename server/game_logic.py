import random
from threading import Lock
from constants import Constants
from logic.snake import Snake
from logic.snakes_food import SnakesFood, create_food_set
from logic.obtacles_gen import generate_obstacles


class GameState:
    def __init__(self):
        self.lock = Lock()
        self.snakes = {}
        self.directions = {}
        self.food = []
        self.obstacles = set()
        self.level = 1
        self.running = True

    def init_player(self, player_id):
        with self.lock:
            initial_pos = (
                random.randint(1, Constants.FIELD_HEIGHT - 2),
                random.randint(1, Constants.FIELD_WIDTH - 2)
            )
            self.snakes[player_id] = Snake(initial_pos, Constants.RIGHT)
            self.directions[player_id] = 'RIGHT'

            # Generate obstacles and food on first player
            if len(self.snakes) == 1:
                self.obstacles = generate_obstacles(None, None)
                self.food = create_food_set([], self.obstacles, 100)

    def update(self):
        with self.lock:
            # Move all snakes
            for player_id, snake in self.snakes.items():
                direction = self.directions.get(player_id, 'RIGHT')
                snake.update_direction(direction)

                next_head = snake.get_next_head()

                # Check collisions
                if (next_head in self.obstacles or
                        any(next_head in s.body for pid, s in
                            self.snakes.items() if pid != player_id)):
                    self.reset_player(player_id)
                    continue

                # Check food
                eaten = None
                for food in self.food:
                    if next_head == food.position:
                        eaten = food
                        break

                snake.move(grow=bool(eaten))

                if eaten:
                    self.food.remove(eaten)
                    self.food.extend(create_food_set(
                        [pos for s in self.snakes.values() for pos in s.body],
                        self.obstacles, 1
                    ))

    def reset_player(self, player_id):
        initial_pos = (
            random.randint(1, Constants.FIELD_HEIGHT - 2),
            random.randint(1, Constants.FIELD_WIDTH - 2)
        )
        self.snakes[player_id] = Snake(initial_pos, Constants.RIGHT)
        self.directions[player_id] = 'RIGHT'

    def get_state(self):
        with self.lock:
            return {
                'snakes': {pid: s.body for pid, s in self.snakes.items()},
                'food': [{'position': f.position, 'type': f.food_type} for f in
                         self.food],
                'obstacles': list(self.obstacles),
                'size': (Constants.FIELD_HEIGHT, Constants.FIELD_WIDTH),
                'level': self.level
            }