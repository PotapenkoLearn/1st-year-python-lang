import random
import tkinter as tk

from figure import LineFigure, CornerFigure

CELL_SIZE = 256  # размер клетки в пикселях
BOARD_SIZE = 4  # 10x10


def draw_grid(canvas):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cls = random.choice([LineFigure, CornerFigure])

            figure = cls(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, canvas)

            figure.draw()

            canvas.tag_bind(figure.image_id, "<Button-1>", figure.rotate)


def draw_game():
    root = tk.Tk()

    root.title('Light\'em up!')

    canvas_width = BOARD_SIZE * CELL_SIZE
    canvas_height = BOARD_SIZE * CELL_SIZE

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, highlightthickness=0, bd=0)
    canvas.pack(padx=10, pady=10)

    draw_grid(canvas)

    root.mainloop()


def print_matrix(matrix):
    for row in matrix:
        result = []

        for col in row:
            if col.type == "line":
                if col.rotation % 180 == 0:
                    result.append(f"- {col.lighting}")
                else:
                    result.append(f"| {col.lighting}")

            if col.type == "corner":
                if col.rotation == 0:
                    result.append(f"└ {col.lighting}")
                elif col.rotation == 90:
                    result.append(f"┌ {col.lighting}")
                elif col.rotation == 180:
                    result.append(f"┐ {col.lighting}")
                elif col.rotation == 270:
                    result.append(f"┘ {col.lighting}")

        print(result)

        result.clear()


# 11 - 01/21 10/12

DIRECTION_COORDINATES = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}

DIRECTION_REVERSE = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


def rotate(matrix, r, c):
    # Создаём свежую visited-матрицу
    visited = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    # Сброс подсветки и подготовка поля
    for row in matrix:
        for col in row:
            col.lighting = False

    # Поворачиваем нужную фигуру
    matrix[r][c].rotate()

    # depth first search
    def dfs(row_start, col_start):
        # Если x (row) выходит за пределы границ, не рассматриваем
        if row_start < 0 or row_start >= BOARD_SIZE:
            return

        # Если y (col) выходит за пределы границ, не рассматриваем
        if col_start < 0 or col_start >= BOARD_SIZE:
            return

        # Если сосед уже был рассмотрен, пропускаем
        if visited[row_start][col_start]:
            return

        figure = matrix[row_start][col_start]

        figure.lighting = True

        visited[row_start][col_start] = True

        for direction in figure.get_connections():
            d_row, d_col = DIRECTION_COORDINATES[direction]
            n_row, n_col = row_start + d_row, col_start + d_col

            # Если x (row) выходит за пределы границ, не рассматриваем
            if n_row < 0 or n_row >= BOARD_SIZE:
                continue

            # Если y (col) выходит за пределы границ, не рассматриваем
            if n_col < 0 or n_col >= BOARD_SIZE:
                continue

            neighbor = matrix[n_row][n_col]

            if DIRECTION_REVERSE[direction] in neighbor.get_connections():
                dfs(n_row, n_col)

    dfs(0, 0)


def main():
    matrix = []

    for row in range(BOARD_SIZE):
        result = []

        for col in range(BOARD_SIZE):
            cls = LineFigure

            rotations = [0, 90, 180, 270]

            # Слева-Сверху всегда линия
            if row == 0 and col == 0:
                cls = LineFigure
            # Справа-Снизу линия или угол в зависимости от честности строк
            elif row == BOARD_SIZE - 1 and col == BOARD_SIZE - 1:
                cls = LineFigure if BOARD_SIZE % 2 else CornerFigure
            # Слева-Снизу линия или угол в зависимости от честности строк
            elif row == BOARD_SIZE - 1 and col == 0:
                cls = CornerFigure if BOARD_SIZE % 2 else LineFigure
            # По краям углы
            elif col == 0 or col == BOARD_SIZE - 1:
                cls = CornerFigure
            # В остальных случая линии
            else:
                cls = LineFigure

            figure = cls(col, row, random.choice(rotations))

            result.append(figure)

        matrix.append(result)

    rotate(matrix, 0, 0)

    print_matrix(matrix)

    while True:
        row, col = map(int, input("Индекс элемента: ").split())

        rotate(matrix, row, col)

        print_matrix(matrix)


if __name__ == '__main__':
    main()
