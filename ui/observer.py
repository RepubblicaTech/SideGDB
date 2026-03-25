from enum import Enum
from typing import Callable

class SGSignals(Enum):
    SGDB_SIGCREATE = "GDB_SIGCREATE"    # Create a GDB instance
    SGDB_SIGLAUNCH = "UI_SIGSTART"      # Launch the debugger
    SGDB_SIGEND = "SGDB_SIGEND"         # Terminate the debugger/GDBMI

__observers = dict()

def subscribe(signal: SGSignals, function: Callable):
    if (signal not in __observers):
        __observers[signal] = list()

    __observers[signal].append(function)

def unsubscribe(function: Callable):
    for signal in __observers:
        try:
            signal.remove(function)
        except ValueError:
            continue

def notify(signal: SGSignals, **kwargs):
    if (signal not in __observers):
        return -1

    for fun in __observers[signal]:
        fun(**kwargs)
