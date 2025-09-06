from core import Editor
from commands import Command


class DeleteColCommand(Command):
    def __init__(self, editor: Editor, col):
        super().__init__(editor)

        if col <= 0:
            raise ValueError

        self.__col = col - 1

    def _do_execute(self):
        content = self._editor.get_content()

        result = []  # сюда будем складывать новые строки

        for item in content:
            # Проверим, что индекс не выходит за пределы строки
            if len(item) > self.__col:
                new_word = item[:self.__col] + item[self.__col + 1:]  # удаляем символ
            else:
                new_word = item  # если индекс слишком большой — оставляем как есть

            result.append(new_word)  # добавляем обработанное слово в результат

        self._editor.set_content(result)
