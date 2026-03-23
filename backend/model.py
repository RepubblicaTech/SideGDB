from typing import Any, List

from backend import GDBMI

class SideModel:
    currentThreadId: int
    currentBreakpoint: str

    registers: dict
    breakpoints: list[dict]

    variables: list[dict]

    def __init__(self, gdbMI: GDBMI.GdbMI) -> None:
        self.__gdbMI = gdbMI

    def send(self, cmd):
        return self.__gdbMI.sendCmd(cmd)

    def read(self, attempts):
        return self.__gdbMI.readResponse(attempts)

    def readMemory(self, address: str, offset: int = 0, count: int = 1):
        return self.send(f"-data-read-memory-bytes -o {offset} {address} {count}")

    def showStackVariables(self):
        return self.send("-stack-list-locals --all-values")

    def getVariableValue(self, varName: str):
        return self.send(f"-data-evaluate-expression {varName}")

    def threadInfo(self):
        return self.send("-thread-info")

    def getRegisterNames(self):
        return self.send("-data-list-register-names")

    def getRegisterValues(self):
        return self.send("-data-list-register-values x")

    def showUpdatedRegisters(self):
        return self.send("-data-list-changed-registers")

    def setBreakpoint(self, position: str):
        try:
            address = int(position)
            return self.send(f"-break-insert *{hex(address)}")
        except ValueError:
            return self.send(f"-break-insert {position}")

    def delBreakpoint(self, breakpointNumber: int):
        return self.send(f"-break-delete {breakpointNumber}")

    def getBreakpoints(self):
        return self.send("-break-list")

    def continueExecution(self):
        return self.send("-exec-continue")

    def stepOver(self):
        return self.send("-exec-next")

    def nextInstruction(self):
        return self.send("-exec-next-instruction")

    def stepInto(self):
        return self.send("-exec-step")

    def stepInstruction(self):
        return self.send("-exec-step-instruction")

    def stepOut(self):
        return self.send("-exec-finish")

    def disassemble(self, startAddress: int, bytes: int):
        endAddress = startAddress + bytes
        return self.send(f"-data-disassemble -s {startAddress} -e {endAddress}")

    def selectResponse(self, gdbMIResponse: dict | List[dict], *keys: tuple[str, Any]) -> dict:
        keysCount = len(keys)
        finds = 0

        if (type(gdbMIResponse) is list):
            for r in gdbMIResponse:
                selected = self.selectResponse(r, *keys)
                if (selected != {}):
                    return selected
        elif (type(gdbMIResponse) is dict):
            for key in keys:
                if (gdbMIResponse.get(key[0]) == key[1]):
                    finds += 1

            if (finds == keysCount):
                return gdbMIResponse

        return {}
