from typing import ClassVar

from pygdbmi.gdbcontroller import GdbController


class GdbMI(GdbController):
    GDBMI_TOKENS: ClassVar[dict[str, int]] = {
        "COD": 00,
        "CPU": 10,
        "SYM": 20,
        "MEM": 30
    }

    def __init__(self, gdbArgs: list[str] | None):
        gdbCommand = ["gdb", "--interpreter=mi2"]

        if (gdbArgs):
            gdbCommand.extend(gdbArgs)

        super().__init__(gdbCommand)
