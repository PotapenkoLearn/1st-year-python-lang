from commands import Command


class History:
    def __init__(self):
        self.history: list[Command] = []

    def push(self, command: Command):
        self.history.append(command)

    def pop(self):
        return self.history.pop() if self.history else None
