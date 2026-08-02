from typing import List, Optional
from pygdbmi.gdbcontroller import GdbController

class GdbMI(GdbController):
    GDBMI_TOKENS = {
        "COD": 00,
        "CPU": 10,
        "SYM": 20,
        "MEM": 30
    }

    def __init__(self, gdbArgs: Optional[List[str]]):
        gdbCommand = ["gdb", "--interpreter=mi2"]

        if (gdbArgs):
            gdbCommand.extend(gdbArgs)

        super().__init__(gdbCommand)
