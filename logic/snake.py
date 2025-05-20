"""Snake: Класс, реализующий логику змейки в игре."""


class Snake:
    def __init__(self, initial_position, initial_direction):
        """__init__: Инициализирует змейку с
        начальной позицией и направлением."""

        self.body = [initial_position]
        self.direction = initial_direction

    def update_direction(self, new_direction):
        """update_direction: Обновляет направление движения змейки."""

        self.direction = new_direction

    def get_next_head(self):
        """get_next_head: Возвращает следующую позицию головы змейки."""

        head = self.body[0]
        return head[0] + self.direction[0], head[1] + self.direction[1]

    def move(self, grow=False):
        """move: Перемещает змейку, с возможностью роста
        и обработки столкновений."""

        new_head = self.get_next_head()
        self.body.insert(0, new_head)

        if new_head in self.body[1:]:
            self.cut_tail(new_head)

        if not grow and len(self.body) > 1:
            self.body.pop()

    def cut_tail(self, head):
        """cut_tail: Обрезает хвост змейки при столкновении с самой собой."""

        index = self.body.index(head)
        self.body = self.body[:max(1, index)]

    def get_length(self):
        """get_length: Возвращает текущую длину змейки."""

        return len(self.body)
