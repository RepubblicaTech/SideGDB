from typing import Any
from pygdbmi import constants
from pygdbmi.gdbcontroller import GdbController

from threading import Lock

from loguru import logger

class GdbMI:
    GDBMI_TOKENS = {
        "COD": 00,
        "CPU": 10,
        "SYM": 20,
        "MEM": 30
    }

    def __init__(self, gdbArgs: list[str] | None):
        gdbCommand = ["gdb", "--interpreter=mi2"]

        if (gdbArgs is not None):
            gdbCommand.extend(gdbArgs)

        self.gdbmi = GdbController(command=gdbCommand)
        self.lock = Lock()

    def readResponse(self, attempts: int):
        att = attempts
        responses = {}
        self.lock.acquire()
        while True:
            try:
                responses = self.gdbmi.get_gdb_response(timeout_sec=1)
                break
            except constants.GdbTimeoutError:
                logger.debug("Waiting...")
                if (att > 0):
                    att -= 1
                    continue

                if (att == -1):
                    continue

                logger.warning("No more attempts.")
                break

        self.lock.release()
        return responses

    # TODO: queue commands
    def sendCmd(self, command: str):
        self.lock.acquire()
        resp = self.gdbmi.write(f"{command}")
        self.lock.release()

        return resp

    def readMemory(self, address: str, offset: int = 0, count: int = 1):
        return self.sendCmd(f"-data-read-memory-bytes -o {offset} {address} {count}")

    def showStackVariables(self):
        return self.sendCmd("-stack-list-locals --all-values")

    def getVariableValue(self, varName: str):
        return self.sendCmd(f"-data-evaluate-expression {varName}")

    def threadInfo(self):
        return self.sendCmd("-thread-info")

    def getRegisterNames(self):
        return self.sendCmd("-data-list-register-names")

    def getRegisterValues(self):
        return self.sendCmd("-data-list-register-values x")

    def showUpdatedRegisters(self):
        return self.sendCmd("-data-list-changed-registers")

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

    def terminate(self):
        return self.gdbmi.exit()
