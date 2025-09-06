import pytest

from main import read_data_from_file, calculate_statistics
from splitter import split_data

CONTENT = "time,value\n1,2\n2,3\n3,4\n6,7"
ROWS = [["1", "2"], ["2", "3"], ["3", "4"], ["6", "7"]]


def test_file_not_found_error(tmp_path):
    # Создаем с помощью фикстуры tmp_path путь к тестовому файлу
    file = tmp_path / "test.csv"

    with pytest.raises(FileNotFoundError, match="Error: file not found"):
        read_data_from_file(str(file))


def test_file_permission_error(tmp_path):
    # Создаем с помощью фикстуры tmp_path путь к тестовому файлу
    file = tmp_path / "test.csv"
    # Создаем сам файл
    file.touch()
    # Меняем права доступа, что бы никто не смог читать файл
    file.chmod(000)

    try:
        with pytest.raises(PermissionError, match="Error: permission denied"):
            read_data_from_file(str(file))
    finally:
        file.chmod(755)


def test_file_invalid_extension(tmp_path):
    # Создаем с помощью фикстуры tmp_path путь к тестовому файлу
    file = tmp_path / "test.txt"
    # Создаем сам файл
    file.touch()

    with pytest.raises(ValueError, match="Error: invalid file extension"):
        read_data_from_file(str(file))


def test_data_single_column(tmp_path):
    file = tmp_path / "test.csv"

    file.write_text(CONTENT + "\n3")

    with pytest.raises(ValueError, match="Error: invalid csv format"):
        read_data_from_file(str(file))


def test_data_invalid(tmp_path):
    file = tmp_path / "test.csv"

    file.write_text("test^value\n4.1%@52")

    with pytest.raises(ValueError, match="Error: invalid csv format"):
        read_data_from_file(str(file))


def test_data_correct_split():
    chunks = split_data(ROWS, 3)

    valid = [[(1.0, 2.0), (2.0, 3.0)], [(3.0, 4.0)], [(6.0, 7.0)]]

    assert chunks == valid


def test_data_correct_split_length():
    assert len(split_data(ROWS, 3)) == 3


def test_statistics_correct():
    chunk = [(1.0, 2.0), (2.0, 3.0)]

    statistics = calculate_statistics(chunk)

    assert statistics["count"] == 2
    assert statistics["mean"] == 2.5
    assert statistics["mode"] == 2.0
    assert statistics["median"] == 2.5


def test_zero_interval():
    rows = [["1", "2"], ["3", "4"]]

    with pytest.raises(ZeroDivisionError, match="Error: zero division"):
        split_data(rows, 0)


def test_identical_values():
    chunk = [(0, 5), (1, 5), (2, 5), (3, 5)]

    statistics = calculate_statistics(chunk)

    assert statistics["mode"] == 5
    assert statistics["median"] == 5
    assert statistics["mean"] == 5
