from robot import Robot


def main():
    robot = Robot(100, 100)

    for command in open("commands.txt", "r"):
        # Обработка ввода команды "Назад" без указания багов
        if command.strip() == "B":
            robot.back()
            continue

        # Парсим введенную команду
        parts = command.split(",")

        if len(parts) != 2:
            print(f"Ошибка: неизвестная команда: {command}")
            return

        direction, steps = parts[0], parts[1]

        if direction == "B":
            robot.back(int(steps))
        else:
            robot.move(direction, int(steps))

    for pos in robot.history_movement[1:]:
        print(f"{pos[0]},{pos[1]}")

main()
