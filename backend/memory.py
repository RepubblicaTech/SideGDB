from backend.GdbMi import GdbMI, GdbMIManager

class MemoryManager(GdbMIManager):

    def __init__(self, gdbMI: GdbMI):
        super().__init__(gdbMI)
        self.GDBMI_TOKEN = "MEM"

    def readMemory(self, address: str, offset: int = 0, count: int = 1):
        return self.sendCmd(f"-data-read-memory-bytes -o {offset} {address} {count}")
