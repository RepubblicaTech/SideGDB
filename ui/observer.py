from enum import Enum
from typing_extensions import Callable


class SGSignals(Enum):
    SGDB_SIGCREATE = "GDB_SIGCREATE"
    SGDB_SIGLAUNCH = "GDB_SIGSTART"
    SGDB_SIGEND = "GDB_SIGEND"

observers = dict()

def subscribe(signal: SGSignals, function: Callable):
    if (signal not in observers):
        observers[signal] = list()

    observers[signal].append(function)

def unsubscribe(function: Callable):
    for signal in observers:
        try:
            signal.remove(function)
        except ValueError:
            continue

def notify(signal: SGSignals, **kwargs):
    if (signal not in observers):
        return -1

    for fun in observers[signal]:
        fun(**kwargs)
