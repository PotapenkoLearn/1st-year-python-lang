from math import floor
from collections import defaultdict

def split_data(rows, interval):
    intervals = defaultdict(list)

    try:
        for row in rows:
            time = float(row[0])
            value = float(row[1])

            key = floor(time / interval) * interval

            intervals[key].append((time, value))
    except ZeroDivisionError:
        raise ZeroDivisionError("Error: zero division")


    return [intervals[key] for key in sorted(intervals)]