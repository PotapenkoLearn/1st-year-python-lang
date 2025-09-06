from .snapshot import Snapshot


class Editor:
    def __init__(self, filepath):
        self.__content: list[str] = []
        self.__filepath = filepath

        self.load_file()

    def get_content(self):
        return self.__content.copy()

    def set_content(self, content: list[str]):
        self.__content = content.copy()

    def create_snapshot(self):
        return Snapshot(self, self.__content)

    def load_file(self):
        try:
            with open(self.__filepath, 'r', encoding='utf-8') as f:
                self.__content = f.read().splitlines()
        except FileNotFoundError:
            self.__content = []

    def save_file(self):
        with open(self.__filepath, 'w', encoding='utf-8') as f:
            for line in self.__content:
                f.write(line + '\n')
