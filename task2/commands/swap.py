from core import Editor
from commands import Command


class SwapCommand(Command):
    def __init__(self, editor: Editor, row_1, row_2):
        super().__init__(editor)

        if row_1 <= 0 or row_2 <= 0 or row_1 == row_2:
            raise ValueError

        self.__row_1 = row_1 - 1
        self.__row_2 = row_2 - 1

    def _do_execute(self):
        content = self._editor.get_content()

        if self.__row_1 not in range(len(content)):
            raise ValueError(f"Строка {self.__row_1 + 1} не найдена.")

        if self.__row_2 not in range(len(content)):
            raise ValueError(f"Строка {self.__row_2 + 1} не найдена.")

        content[self.__row_1], content[self.__row_2] = content[self.__row_2], content[self.__row_1],

        self._editor.set_content(content)
