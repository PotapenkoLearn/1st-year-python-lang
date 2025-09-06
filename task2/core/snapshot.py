from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .editor import Editor

class Snapshot:
    def __init__(self, editor: Editor, content):
        self.__editor = editor
        self.__content = content.copy()

    def restore(self):
        self.__editor.set_content(self.__content)
