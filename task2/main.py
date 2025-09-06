import cmd
import shlex
import sys

from core import Editor, History
from commands import Command, InsertCommand, DeleteCommand, DeleteRowCommand, DeleteColCommand, SwapCommand

INVALID_COMMAND_ERROR = "Команда введена некорректно."


def parse(arg: str) -> dict:
    args = shlex.split(arg)
    parsed = {}
    key = None

    for arg in args:
        if arg.startswith('-') and not arg.startswith('--'):
            key = arg.lstrip('-')
            parsed[key] = True  # по умолчанию — просто флаг
        elif key:
            parsed[key] = arg
            key = None
    return parsed


class TextEditorShell(cmd.Cmd):

    def __init__(self):
        super().__init__()

        self.editor = Editor("file.txt")
        self.history = History()

    def execute_command(self, command: Command):
        try:
            command.execute()

            self.history.push(command)
        except ValueError as e:
            print(e)

    # Вставка текста
    def do_insert(self, arg):
        try:
            params = parse(arg)

            text = params.get('t')
            row = params.get('r')
            col = params.get('c')

            row = int(row) if isinstance(row, str) else None
            col = int(col) if isinstance(col, str) else None

            if isinstance(text, str) and len(text) > 0:
                self.execute_command(InsertCommand(self.editor, text, row, col))
            else:
                raise ValueError
        except (ValueError, TypeError):
            print(INVALID_COMMAND_ERROR)

    # Удаление содержимого
    def do_del(self, _):
        self.execute_command(DeleteCommand(self.editor))

    # Удаление строки
    def do_delrow(self, arg):
        try:
            params = parse(arg)

            row = params.get('r')

            row = int(row) if isinstance(row, str) else 0

            self.execute_command(DeleteRowCommand(self.editor, row))
        except (ValueError, TypeError):
            print(INVALID_COMMAND_ERROR)

    # Удаление колонки
    def do_delcol(self, arg):
        try:
            params = parse(arg)

            col = params.get('c')

            col = int(col) if isinstance(col, str) else 0

            self.execute_command(DeleteColCommand(self.editor, col))
        except (ValueError, TypeError):
            print(INVALID_COMMAND_ERROR)

    # Изменение порядка строк
    def do_swap(self, arg):
        try:
            params = parse(arg)

            row_1 = params.get('r1')
            row_2 = params.get('r2')

            row_1 = int(row_1) if isinstance(row_1, str) else 0
            row_2 = int(row_2) if isinstance(row_2, str) else 0

            self.execute_command(SwapCommand(self.editor, row_1, row_2))
        except (ValueError, TypeError):
            print(INVALID_COMMAND_ERROR)

    # Отменить действие
    def do_undo(self, _):
        command = self.history.pop()

        if command:
            command.undo()

    def do_save(self, _):
        self.editor.save_file()

    # Просмотр содержимого
    def do_show(self, _):
        for i, word in enumerate(self.editor.get_content(), start=1):
            print(f"{i}. {word}")

    # Выйти из редактора
    def do_exit(self, _):
        sys.exit()

    def do_help(self, _):
        pass


if __name__ == '__main__':
    TextEditorShell().cmdloop()
