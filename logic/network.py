import curses
import json

from constants import Constants


def encode(data):
    json_data = json.dumps(data).encode('utf-8')
    return json_data + Constants.MESSAGE_DELIMITER


def decode_single(data):
    return json.loads(data.decode('utf-8'))


def decode_stream(buffer):
    messages = []
    parts = buffer.split(Constants.MESSAGE_DELIMITER)

    # Последняя часть может быть неполной
    incomplete = parts.pop() if parts else b''

    for part in parts:
        if part:  # Пропускаем пустые части
            try:
                messages.append(decode_single(part))
            except json.JSONDecodeError:
                pass  # Игнорируем некорректные сообщения

    return messages, incomplete


KEYS = {
    ord('w'): 'UP',
    ord('a'): 'LEFT',
    ord('s'): 'DOWN',
    ord('d'): 'RIGHT',
    ord('ц'): 'UP',
    ord('ф'): 'LEFT',
    ord('ы'): 'DOWN',
    ord('в'): 'RIGHT',
    curses.KEY_UP: 'UP',
    curses.KEY_LEFT: 'LEFT',
    curses.KEY_DOWN: 'DOWN',
    curses.KEY_RIGHT: 'RIGHT'
}
