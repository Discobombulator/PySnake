from constants import Constants


class Snake:
    def __init__(self, initial_position, initial_direction):
        self.body = [initial_position]
        # Убедимся, что направление - это кортеж, а не строка
        if isinstance(initial_direction, str):
            self.direction = Constants.DIRECTIONS.get(initial_direction,
                                                      Constants.RIGHT)
        else:
            self.direction = initial_direction

    def update_direction(self, new_direction):
        # Аналогично для нового направления
        if isinstance(new_direction, str):
            self.direction = Constants.DIRECTIONS.get(new_direction,
                                                      self.direction)
        else:
            self.direction = new_direction

    # Остальные методы без изменений
    def get_next_head(self):
        head = self.body[0]
        return (head[0] + self.direction[0],
                head[1] + self.direction[1])

    def move(self, grow=False):
        new_head = self.get_next_head()
        self.body.insert(0, new_head)

        if new_head in self.body[1:]:
            self.cut_tail(new_head)

        if not grow and len(self.body) > 1:
            self.body.pop()

    def cut_tail(self, head):
        index = self.body.index(head)
        self.body = self.body[:max(1, index)]

    def get_length(self):
        return len(self.body)
