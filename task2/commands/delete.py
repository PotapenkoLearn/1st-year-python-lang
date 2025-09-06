from core import Editor
from commands import Command


class DeleteCommand(Command):
    def __init__(self, editor: Editor):
        super().__init__(editor)

    def _do_execute(self):
        self._editor.set_content([])
