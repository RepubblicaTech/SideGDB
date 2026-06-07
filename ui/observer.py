from typing import Callable, List


class Signal:
    def __init__(self):
        self.callables: List[Callable] = list()

    def connectHandler(self, callable: Callable):
        self.callables.append(callable)

    def removeHandler(self, callable: Callable):
        try:
            self.callables.remove(callable)
        except ValueError:
            return

    def trigger(self, *args):
        for callable in self.callables:
            callable(*args)
