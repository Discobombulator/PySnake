import socket
import json
import curses
from scr.constants import Constants
from scr.logic.snake import Snake
from scr.logic.snakes_food import SnakesFood
from scr.visual.game_board import draw_board

SERVER_IP = '127.0.0.1'
PORT = 12345


def main(stdscr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))
    sock.setblocking(False)

    curses.curs_set(0)
    stdscr.nodelay(True)
    current_direction = Constants.RIGHT

    while True:
        # Обработка ввода
        key = stdscr.getch()
        new_dir = None

        if key == curses.KEY_UP:
            new_dir = Constants.UP
        elif key == curses.KEY_DOWN:
            new_dir = Constants.DOWN
        elif key == curses.KEY_LEFT:
            new_dir = Constants.LEFT
        elif key == curses.KEY_RIGHT:
            new_dir = Constants.RIGHT

        if new_dir and new_dir != current_direction:
            sock.sendall(json.dumps(new_dir).encode())
            current_direction = new_dir

        # Получение состояния игры
        try:
            data = sock.recv(4096)
            if data:
                game_state = json.loads(data.decode())
                snakes = {int(k): Snake(v[0], v[0]) for k, v in
                          game_state['snakes'].items()}
                draw_board(
                    snakes[0],
                    [SnakesFood(pos, 1) for pos in game_state['food']],
                    stdscr,
                    level=game_state['level'],
                    obstacles=set(tuple(o) for o in game_state['obstacles'])
                )
        except:
            pass

        curses.napms(50)


if __name__ == "__main__":
    curses.wrapper(main)