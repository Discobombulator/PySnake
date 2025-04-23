import curses
import json

# Example implementation for network.py if not already correct
import json

def encode(data):
    """Encode data to bytes for network transmission"""
    return json.dumps(data).encode('utf-8')

def decode(data):
    """Decode bytes from network to Python object"""
    return json.loads(data.decode('utf-8'))

KEYS = {
    ord('w'): 'UP',
    ord('a'): 'LEFT',
    ord('s'): 'DOWN',
    ord('d'): 'RIGHT',
    ord('ц'): 'UP',    # Russian keyboard layout
    ord('ф'): 'LEFT',
    ord('ы'): 'DOWN',
    ord('в'): 'RIGHT',
    curses.KEY_UP: 'UP',
    curses.KEY_LEFT: 'LEFT',
    curses.KEY_DOWN: 'DOWN',
    curses.KEY_RIGHT: 'RIGHT'
}