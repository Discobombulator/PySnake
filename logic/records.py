"""GameRecords: Хранит и управляет рекордами игры (ТОП-3)."""


class GameRecords:

    def __init__(self):
        """__init__: Инициализирует список
         рекордов и загружает данные из файла."""

        self._data = [0, 0, 0]
        self.load_data()

    def get_data(self):
        """get_data: Возвращает текущий список рекордов."""

        return self._data

    def set_data(self, new_score):
        """set_data: Добавляет новый результат, сохраняя только ТОП-3."""

        self._data.append(new_score)
        self._data = sorted(self._data, reverse=True)[:3]
        self.save_data()

    def save_data(self):
        """save_data: Сохраняет рекорды в файл 'rec.txt'."""

        with open("rec.txt", "w") as file:
            for score in self._data:
                file.write(str(score) + "\n")

    def load_data(self):
        """load_data: Загружает рекорды из файла '
        rec.txt' (если существует)."""

        try:
            with open("rec.txt", "r") as file:
                self._data = [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            self._data = [0, 0, 0]
