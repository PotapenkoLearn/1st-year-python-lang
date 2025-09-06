from core import Editor
from commands import Command


class InsertCommand(Command):
    def __init__(self, editor: Editor, text: str, row: int = None, col: int = None):
        super().__init__(editor)

        self.__text = text
        self.__row = row - 1 if isinstance(row, int) else None
        self.__col = col - 1 if isinstance(col, int) else None

    def _do_execute(self):
        content = self._editor.get_content()

        if self.__row is not None and self.__row not in range(len(content)):
            raise ValueError(f"Строка с номером {self.__row + 1} не найдена.")

        if self.__row is None:
            content.append(self.__text)
        else:
            row_text = content[self.__row]

            index = self.__col if self.__col is not None else len(row_text)

            content[self.__row] = row_text[:index] + self.__text + row_text[index:]

        self._editor.set_content(content)
