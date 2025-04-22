from controllers.level_controller import level_controller
from logic.records import GameRecords


def start_work(std):
    records = GameRecords()
    records.load_data()
    data = records.get_data()
    std.clear()

    std.addstr(0, 0, "Добро пожаловать в игру Snake")
    std.addstr(1, 0, "Текущиий топ:")
    std.addstr(2, 0, "  первое место - " + str(data[0]))
    std.addstr(3, 0, "  второе место - " + str(data[1]))
    std.addstr(4, 0, "  третье место - " + str(data[2]))
    std.addstr(5, 0, "_________________________________________")
    std.addstr(6, 0, "                                         ")
    std.addstr(7, 0, "Для начала выберите уровень сложности")
    std.addstr(8, 0, "1 - легкий")
    std.addstr(9, 0, "2 - средний")
    std.addstr(10, 0, "3 - сложный")
    std.addstr(11, 0, " ")
    std.addstr(12, 0, "Уровень: ")

    std.refresh()
    result = level_controller(std)

    return result
