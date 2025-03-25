class GameRecords:
    def __init__(self):
        self._data = [0, 0, 0]
        self.load_data()

    def get_data(self):
        return self._data

    def set_data(self, new_score):
        self._data.append(new_score)
        self._data = sorted(self._data, reverse=True)[:3]
        self.save_data()

    def save_data(self):
        with open("rec.txt", "w") as file:
            for score in self._data:
                file.write(str(score) + "\n")

    def load_data(self):
        try:
            with open("rec.txt", "r") as file:
                self._data = [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            self._data = [0, 0, 0]
