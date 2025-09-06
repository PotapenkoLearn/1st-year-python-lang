from core import Editor
from commands import Command


class DeleteRowCommand(Command):
    def __init__(self, editor: Editor, row):
        super().__init__(editor)

        if row <= 0:
            raise ValueError

        self.__row = row - 1

    def _do_execute(self):
        content = self._editor.get_content()

        if self.__row not in range(len(content)):
            raise ValueError(f"Строка с номером {self.__row + 1} не найдена.")

        content.pop(self.__row)

        self._editor.set_content(content)
