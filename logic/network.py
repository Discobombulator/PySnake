import curses
import json

# Константа для разделения сообщений
MESSAGE_DELIMITER = b'\n\n'


def encode(data):
    """Кодирует данные в JSON и добавляет разделитель"""
    json_data = json.dumps(data).encode('utf-8')
    return json_data + MESSAGE_DELIMITER


def decode_single(data):
    """Декодирует одно сообщение из JSON"""
    return json.loads(data.decode('utf-8'))


def decode_stream(buffer):
    """Декодирует несколько сообщений из буфера"""
    messages = []
    parts = buffer.split(MESSAGE_DELIMITER)

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
