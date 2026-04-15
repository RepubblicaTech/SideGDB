from typing import Any, List

from PySide6.QtGui import QStandardItem, QStandardItemModel
from loguru import logger

from backend import GDBMI

class SideModel:
    currentToken: int = 0
    currentThreadId: int
    currentBreakpoint: str

    registers: dict
    breakpointsStandardModel: QStandardItemModel

    variables: list[dict]

    def __init__(self, gdbMI: GDBMI.GdbMI) -> None:
        self.__gdbMI = gdbMI

        self.breakpointsStandardModel = QStandardItemModel(0, 2)

    def send(self, cmd):
        r =  self.__gdbMI.sendCmd(f"{self.currentToken}{cmd}")
        self.currentToken += 1
        return r

    def read(self, attempts):
        return self.__gdbMI.readResponse(attempts)

    def setBreakpoint(self, where: str):
        if (not str):
            return None

        return self.send(f"-break-insert {where}")

    def getBreakpointsList(self) -> List[dict[str, Any]] | None:
        responses =  self.send("-break-list")
        r = self.selectResponse(responses, ("token", self.currentToken - 1))
        if (not r):
            logger.warning(f"No response with token {self.currentToken - 1}")
            return None
        payload = r.get("payload", None)
        if ((not payload) or ("BreakpointTable" not in payload) or ("body" not in payload["BreakpointTable"])):
            logger.debug("No BreakpointTable given.")
            return None
        body = list(payload["BreakpointTable"]["body"])
        if (len(body) < 1):
            logger.debug("No breakpoints yet.")
            return None

        breakpointsList = list()
        for b in body:
            breakpoint = dict(b)

            bDict = {
                "number": breakpoint.get("number"),
                "enabled": True if (breakpoint.get("enabled") == "y") else False,
                "addr": breakpoint.get("addr", None),
                # Optional
                "func": breakpoint.get("func", None),
                "file": breakpoint.get("file", None),
                "fullPath": breakpoint.get("fullname", None),
                "line": breakpoint.get("line", None),
            }
            breakpointsList.append(bDict)

        return breakpointsList

    def loadBreakpointsListToModel(self):
        list = self.getBreakpointsList()
        if (not list):
            return

        self.breakpointsStandardModel.clear()
        for b in list:
            bNo = QStandardItem(str(b.get("number", "XX")))
            whereStr = f"{b.get("func", b.get("addr"))}[{b.get("file", "/???.?")}:{b.get("line", "??")}]"
            where = QStandardItem(whereStr)
            self.breakpointsStandardModel.appendRow([bNo, where])

    def terminate(self):
        self.__gdbMI.exit()

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
