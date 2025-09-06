MAX_WIDTH = 100
MAX_HEIGHT = 100

RobotCommand = tuple[str, int]

def reverse_direction(direction: str):
    if direction == "R":
        return "L"
    elif direction == "L":
        return "R"
    elif direction == "U":
        return "D"
    elif direction == "D":
        return "U"


class Robot:
    def __init__(self, max_width: int = MAX_WIDTH, max_height: int = MAX_HEIGHT):
        self.width = max_width
        self.height = max_height
        self.position = [1, 1]
        self.history_movement = [[1, 1]]

        self.history_commands: list[RobotCommand] = []

    def move(self, direction: str, steps: int, write_command_history = True):
        if write_command_history:
            self.history_commands.append((direction, steps))

        # Итерируемся по количеству шагов для корректной записи в историю позиции робота
        for n in range(steps):
            # Создаем копию текущих координат для дальнейшей проверки выхода за границы поля
            new_position = self.position.copy()

            # Изменяем координаты в соответствии с переданным направлением
            if direction == "R":
                new_position[0] += 1
            elif direction == "L":
                new_position[0] -= 1
            elif direction == "U":
                new_position[1] -= 1
            elif direction == "D":
                new_position[1] += 1

            # Если новые координаты выходят за границы поля, то выходим из функции не изменяя
            # Текущего положения робота
            if not (1 <= new_position[0] <= self.width and 1 <= new_position[1] <= self.height):
                print("Ошибка: выход за границы поля")
                return False

            # Меняем текущие координаты и записываем шаг в историю перемещения
            self.position = new_position
            self.history_movement.append(new_position.copy())

        return True

    def back(self, steps: int = 1):
        # Если количество возвращений назад больше, чем было задано команд роботу, то не выполняем
        # это возвращение
        if steps > len(self.history_commands):
            print(f"Ошибка: невозможно вернуться на {steps} шаг(а|ов) назад")
            return False

        for n in range(steps):
            # Берем последнюю команду робота, достаем из нее направление и количество шагов
            # Направление инвертируем для корректного возвращения назад
            d, s = reverse_direction(self.history_commands[-1][0]), self.history_commands[-1][1]

            # Передвигаем робота, но не учитываем эти перемещения в истории команд
            self.move(d, s, False)

            # Удаляем последнюю команду, что бы не было зацикливания
            self.history_commands = self.history_commands[:-1]