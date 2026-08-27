from collections.abc import Callable


class Signal:
    def __init__(self):
        self.callables: list[Callable[..., None]] = []

    def connectHandler(self, callable: Callable[..., None]):
        self.callables.append(callable)

    def removeHandler(self, callable: Callable[..., None]):
        try:
            self.callables.remove(callable)
        except ValueError:
            return

    def trigger(self, *args: ...):
        for callable in self.callables:
            callable(*args)
