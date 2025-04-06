import curses
import time
import random
from scr.constants import Constants
from scr.end_scene.end_scene import end_print
from scr.game_scene.game_controller import game_controller, check_end_game
from scr.game_scene.game_board import draw_board, generate_obstacles
from scr.game_scene.snakes_food import create_food
from scr.game_scene.snake import Snake
from scr.start_scene.records import GameRecords


class GameState:
    START = "start"
    PLAY = "play"
    GAME_OVER = "game_over"

    def __init__(self, std):
        self.state = GameState.START  # Начинаем с состояния "START"
        self.std = std
        self.snake = None
        self.food = None
        self.level = 1
        self.records = GameRecords()

    def start(self):
        """Главная логика игры с конечным автоматом"""
        while True:
            if self.state == GameState.START:
                self.show_start_screen()
            elif self.state == GameState.PLAY:
                self.play_game()
            elif self.state == GameState.GAME_OVER:
                self.show_game_over_screen()

    def show_start_screen(self):
        """Показываем экран с выбором уровня"""
        self.std.clear()
        self.std.addstr(0, 0, "Добро пожаловать в игру Snake")
        self.std.addstr(1, 0, "Для начала выберите уровень сложности")
        self.std.addstr(2, 0, "1 - легкий")
        self.std.addstr(3, 0, "2 - средний")
        self.std.addstr(4, 0, "3 - сложный")
        self.std.addstr(5, 0, "Для выхода нажмите [q]")
        self.std.refresh()

        key = self.std.getch()
        if key in [ord('1'), ord('!')]:
            self.level = 1
            self.state = GameState.PLAY
        elif key in [ord('2'), ord('@')]:
            self.level = 2
            self.state = GameState.PLAY
        elif key in [ord('3'), ord('#')]:
            self.level = 3
            self.state = GameState.PLAY
        elif key in [ord('q'), ord('й')]:
            return  # Выход из игры

    def play_game(self):
        """Основной игровой цикл"""
        self.snake = Snake((Constants.FIELD_HEIGHT // 2, Constants.FIELD_WIDTH // 2), Constants.RIGHT)
        self.food = create_food(self.snake.body)
        obstacles = generate_obstacles(self.snake, self.food, self.level)

        self.std.nodelay(True)
        self.std.timeout(100)

        horizontal_delay = 0.1
        vertical_delay = 0.1 * Constants.SPEED_RATIO

        while True:
            draw_board(self.snake, self.food, self.std, random.randint(1, 2), level=self.level, obstacles=obstacles)
            make_step = game_controller(self.snake.direction, self.std)
            if make_step == "brake":
                self.records.set_data(self.snake.get_length())
                self.state = GameState.GAME_OVER  # Переходим в состояние конца игры
                break
            self.snake.update_direction(make_step)

            next_head = self.snake.get_next_head()

            if check_end_game(next_head, self.std, self.snake, obstacles):
                self.records.set_data(self.snake.get_length())
                self.state = GameState.GAME_OVER  # Переход к состоянию конца игры
                break

            if next_head == self.food.position:
                self.snake.move(grow=True)
                for _ in range(self.food.get_growth() - 1):
                    self.snake.move(grow=True)
                self.food = create_food(self.snake.body)
            else:
                self.snake.move(grow=False)

            # Время ожидания в зависимости от направления змейки
            if self.snake.direction in [Constants.LEFT, Constants.RIGHT]:
                time.sleep(horizontal_delay)
            else:
                time.sleep(vertical_delay)

    def show_game_over_screen(self):
        """Показываем экран конца игры"""
        end_print(self.std, self.snake)
        key = self.std.getch()

        if key in [ord('q'), ord('й')]:
            return  # Выход из игры
        elif key == curses.KEY_ENTER:
            self.state = GameState.START  # Перезапуск игры

