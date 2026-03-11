from typing_extensions import Any
from pygdbmi import constants
from pygdbmi.gdbcontroller import GdbController

from threading import Lock

import logging

class GdbMI:
    GDBMI_TOKENS = {
        "COD": 00,
        "CPU": 10,
        "SYM": 20,
        "MEM": 30
    }

    def __init__(self, gdbArgs: list[str]):
        gdbCommand = ["gdb", "--interpreter=mi2"]

        if (gdbArgs):
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
                logging.debug("Waiting...")
                if (att > 0):
                    att -= 1
                    continue

                if (att == -1):
                    continue

                logging.warn("No more attempts.")
                break

        self.lock.release()
        return responses

    # TODO: queue commands
    def sendCmd(self, command: str):
        self.lock.acquire()
        resp = self.gdbmi.write(f"{command}")
        self.lock.release()

        return resp

    def quit(self):
        return self.sendCmd("-gdb-exit")

# this class can manage a component of the GDB-MI
class GdbMIManager:
    GDBMI_TOKEN = ""

    def __init__(self, gdbMI: GdbMI):
        if (not gdbMI):
            raise ValueError("Where GDBMI class?")

        self.gdbMI = gdbMI

    def token(self):
        return GdbMI.GDBMI_TOKENS[self.GDBMI_TOKEN]

    def sendCmd(self, command: str):
        return self.gdbMI.sendCmd(f"{self.token()}{command}")

    def selectResponse(self, gdbMIResponse: dict | list, *keys: tuple[str, Any]) -> dict:
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
