from typing import List, Optional
from pygdbmi import constants
from pygdbmi.gdbcontroller import GdbController

from threading import Lock

from loguru import logger

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
        self.lock = Lock()

    def sendCmd(self, command: str):
        self.lock.acquire()
        resp = self.write(f"{command}")
        self.lock.release()

        return resp

    def readResponse(self, attempts: int = -1):
        att = attempts
        responses = {}
        self.lock.acquire()
        while True:
            try:
                responses = self.get_gdb_response(timeout_sec=1)
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

    def terminate(self):
        return self.exit()
