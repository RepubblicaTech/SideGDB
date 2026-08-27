from typing import Callable


class Signal:
    def __init__(self):
        self.callables: list[Callable] = list()

    def connectHandler(self, callable):
        self.callables.append(callable)

    def removeHandler(self, callable):
        try:
            self.callables.remove(callable)
        except ValueError:
            return

    def trigger(self, *args):
        for callable in self.callables:
            callable(*args)
