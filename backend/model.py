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

    def send(self, cmd):
        return self.__gdbMI.sendCmd(cmd)

    def read(self, attempts):
        return self.__gdbMI.readResponse(attempts)
