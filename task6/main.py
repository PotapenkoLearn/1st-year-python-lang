import os
import hashlib
from collections import defaultdict


def hash_file(path, block_size=65536):
    hasher = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)

        return hasher.hexdigest()
    except Exception as e:
        print(f"[!] Не удалось прочитать файл: {path} — {e}")
        return None


def find_duplicates(root_dir):
    hashes = defaultdict(list)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_hash = hash_file(full_path)
            if file_hash:
                hashes[file_hash].append(full_path)

    return {h: paths for h, paths in hashes.items() if len(paths) > 1}


def prompt_user(duplicates):
    for file_hash, files in duplicates.items():
        print("\nНайдены дубликаты:")
        for idx, path in enumerate(files, start=1):
            print(f"  [{idx}] {path}")

        while True:
            choice = input("Введите номер файла, который оставить (или нажмите Enter, чтобы пропустить): ")
            if choice.strip() == "":
                print("Пропущено, все файлы сохранены.")
                break
            if choice.isdigit() and 1 <= int(choice) <= len(files):
                keep = files[int(choice) - 1]
                for path in files:
                    if path != keep:
                        try:
                            os.remove(path)
                            print(f"Удалён: {path}")
                        except Exception as e:
                            print(f"[!] Не удалось удалить {path}: {e}")
                break
            else:
                print("Неверный ввод. Повторите попытку.")


def main():
    import sys

    if len(sys.argv) != 2:
        print("Использование: python3 main.py <путь_к_директории>")
        return

    root_dir = sys.argv[1]

    if not os.path.isdir(root_dir):
        print(f"[!] Указанный путь не является директорией: {root_dir}")
        return

    duplicates = find_duplicates(root_dir)

    if not duplicates:
        print("Дубликатов не найдено")
    else:
        prompt_user(duplicates)


if __name__ == "__main__":
    main()
