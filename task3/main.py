import statistics
import csv
import sys
import re

from splitter import split_data


def read_data_from_file(filename):
    if not filename.lower().endswith(".csv"):
        raise ValueError("Error: invalid file extension")

    try:
        with open(filename, newline='') as csvfile:
            content = csvfile.read()

            pattern = r"^time,value\n(\d+(\.\d+)?,\d+(\.\d+)?\n?)*$"

            if not re.fullmatch(pattern, content):
                raise ValueError("Error: invalid csv format")

            # Перематываем файл обратно в начало и читаем снова, уже csv.reader'ом
            csvfile.seek(0)

            return [row for row in csv.reader(csvfile)]
    except FileNotFoundError:
        raise FileNotFoundError("Error: file not found")
    except PermissionError:
        raise PermissionError("Error: permission denied")


def calculate_statistics(chunk):
    values = [v for _, v in chunk]

    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "mode": statistics.mode(values),
        "median": statistics.median(values),
    }


def main():
    if len(sys.argv) < 3:
        print("Использование: python main.py <filename.csv> <interval>")
        return

    filename = sys.argv[1]
    interval = float(sys.argv[2])

    raw_rows = read_data_from_file(filename)

    chunks = split_data(raw_rows[1:], interval)

    for i, chunk in enumerate(chunks):
        if not chunk:
            continue

        start = chunk[0][0]
        end = chunk[-1][0]
        stats = calculate_statistics(chunk)

        print(f"\nОтрезок {i + 1}: от {start} до {end}")

        for key, val in stats.items():
            print(f"  {key}: {val}")


if __name__ == "__main__":
    main()
