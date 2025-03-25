class Snake:
    def __init__(self, initial_position, initial_direction):
        self.body = [initial_position]  # список координат сегментов змеи (голова — первый элемент)
        self.direction = initial_direction  # текущее направление (например, (0, 1) для движения вправо)

    def update_direction(self, new_direction):
        """Обновляет направление движения змеи."""
        self.direction = new_direction

    def get_next_head(self):
        """Возвращает координаты следующей головы змеи."""
        head = self.body[0]
        return (head[0] + self.direction[0], head[1] + self.direction[1])

    def move(self, grow=False):
        """Перемещает змейку: вычисляет новую голову, вставляет её в начало.
        Если grow==False, то убирает последний элемент (хвост)."""
        new_head = self.get_next_head()
        self.body.insert(0, new_head)

        # Если змея врезалась в себя, удаляем всё после точки столкновения
        if new_head in self.body[1:]:
            self.cut_tail(new_head)

        if not grow and len(self.body) > 1:
            self.body.pop()

    def cut_tail(self, head):
        """Оставляет только часть змеи, не затронутую столкновением."""
        index = self.body.index(head)  # Находим, где произошло столкновение
        self.body = self.body[:max(1, index)]  # Гарантируем, что останется хотя бы 1 сегмент

    def get_length(self):
        """Возвращает текущую длину змейки."""
        return len(self.body)
