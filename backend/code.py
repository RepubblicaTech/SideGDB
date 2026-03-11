from backend.gdbmi import GdbMI, GdbMIManager

class CodeManager(GdbMIManager):

    def __init__(self, gdbMI: GdbMI):
        super().__init__(gdbMI)
        self.GDBMI_TOKEN = "COD"

    def setBreakpoint(self, position: str):
        try:
            address = int(position)
            return self.sendCmd(f"-break-insert *{hex(address)}")
        except ValueError:
            return self.sendCmd(f"-break-insert {position}")

    def delBreakpoint(self, breakpointNumber: int):
        return self.sendCmd(f"-break-delete {breakpointNumber}")

    def getBreakpoints(self):
        return self.sendCmd("-break-list")

    def continueExecution(self):
        return self.sendCmd("-exec-continue")

    def stepOver(self):
        return self.sendCmd("-exec-next")

    def nextInstruction(self):
        return self.sendCmd("-exec-next-instruction")

    def stepInto(self):
        return self.sendCmd("-exec-step")

    def stepInstruction(self):
        return self.sendCmd("-exec-step-instruction")

    def stepOut(self):
        return self.sendCmd("-exec-finish")

    def disassemble(self, startAddress: int, bytes: int):
        endAddress = startAddress + bytes
        return self.sendCmd(f"-data-disassemble -s {startAddress} -e {endAddress}")
