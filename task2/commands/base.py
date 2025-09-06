from abc import ABC, abstractmethod

from core import Editor, Snapshot


class Command(ABC):
    def __init__(self, editor: Editor):
        self._editor = editor
        self._snapshot: Snapshot | None = None

    @abstractmethod
    def _do_execute(self):
        pass

    def execute(self):
        self._snapshot = self._editor.create_snapshot()
        self._do_execute()

    def undo(self):
        if self._snapshot is not None:
            self._snapshot.restore()
