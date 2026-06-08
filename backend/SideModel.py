from threading import Thread
from typing import Any, List

from PySide6.QtGui import QStandardItem, QStandardItemModel
from loguru import logger

from backend import GDBMI
from pygdbmi.constants import GdbTimeoutError
from ui.observer import Signal

class SideModel:
    def __init__(self, gdbMI: GDBMI.GdbMI) -> None:
        self.__gdbMI = gdbMI

        self.breakpointsStandardModel = QStandardItemModel(0, 2)
        self.currentToken = 0

        self.miResponseReceived = Signal()
        self.miExecutionChanged = Signal()

    # Request the last token that was sent to GDBMI.
    def token(self):
        return self.currentToken - 1

    def send(self, cmd):
        r =  self.__gdbMI.write(f"{self.currentToken}{cmd}")
        self.currentToken += 1

        self.miResponseReceived.trigger(r)

        match(cmd):
            case str(cmd) if MICommands.MIPREFIX_EXEC in cmd:
                self.getThreadInfoAtExecStopped(r)
            case _:
                pass
        return r

    def read(self, attempts):
        responses = {}
        logger.debug("Waiting for response")
        while True:
            try:
                responses = self.__gdbMI.get_gdb_response()
                break
            except GdbTimeoutError:
                if (attempts > 0):
                    attempts -= 1
                    continue

                if (attempts == -1):
                    continue

                logger.warning("\nNo more attempts.")
                break
        logger.success("\nRead response OK")

        self.miResponseReceived.trigger(responses)
        return responses

    def deleteBreakpoint(self, number):
        return self.send(f"{MICommands.MI_BREAKREM} {number}")

    def setBreakpoint(self, where: str) -> dict | None:
        if (not str):
            return None

        responses = self.send(f"{MICommands.MI_BREAKADD} {where}")
        r = self.selectResponse(responses, ("token", self.token()))
        if (type(r) is not dict):
            return

        if (r.get("message", None) != "done"):
            payload = dict(r["payload"])
            raise RuntimeError(payload.get("msg", r.get("payload", "Unknown error.")))

        payload = r.get("payload", None)
        if ((not payload) or ("bkpt" not in payload)):
            logger.warning("No breakpoint?")
            return None
        bkpt = dict(payload["bkpt"])

        return {
            "number": bkpt.get("number"),
            "enabled": True if (bkpt.get("enabled") == "y") else False,
            "addr": bkpt.get("addr"),
            "where": bkpt.get("func", bkpt.get("at", None)),
            "source": bkpt.get("file", None),
            "sourceFullPath": bkpt.get("fullname", None),
            "line": bkpt.get("line", None)
        }

    def getBreakpointsList(self) -> List[dict[str, Any]] | None:
        responses =  self.send(MICommands.MI_BREAKLIST)
        r = self.selectResponse(responses, ("token", self.token()))
        if (not r):
            logger.warning(f"No response with token {self.token()}")
            return None
        payload = r.get("payload", None)
        if ((not payload) or ("BreakpointTable" not in payload) or ("body" not in payload["BreakpointTable"])):
            logger.warning("No BreakpointTable given.")
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

    def threadInfo(self):
        responses = self.send(MICommands.MI_THREADINF)
        response = self.selectResponse(responses, ("token", self.token()))
        if (not response):
            return {}
        payload = response.get("payload", None)
        if (not payload):
            return {}

        threads = list()
        for thread in payload.get("threads", []):
            threadDict = dict(thread)
            threads.append({
                "id": threadDict.get("id", None),
                "state": threadDict.get("state", "unknown"),
                "frame": threadDict.get("frame", None),
            })
        return {
            "currentThread": payload.get("current-thread-id", None),
            "threads": threads
        }

    def getThreadInfoAtExecStopped(self, execResponse):
        t = Thread(target=lambda: self.read(-1))
        if (self.selectResponse(execResponse, ("message", "stopped")) is None):
            t.start()
            # TODO: check for any input from program (idk how, but at least i don't hang up the whole program in the meanwhile)
            t.join()

        self.miExecutionChanged.trigger(self.threadInfo())

    def continueExecution(self):
        responses = self.send(MICommands.MI_CONTINUE)
        self.getThreadInfoAtExecStopped(responses)

    def stepOver(self):
        responses = self.send(MICommands.MI_STEPNX)
        self.getThreadInfoAtExecStopped(responses)

    def stepInto(self):
        responses = self.send(MICommands.MI_STEPIN)
        self.getThreadInfoAtExecStopped(responses)

    def stepOut(self):
        responses = self.send(MICommands.MI_STEPOUT)
        self.getThreadInfoAtExecStopped(responses)

    def terminate(self):
        self.__gdbMI.exit()

    def selectResponse(self, gdbMIResponse: dict | List[dict], *keys: tuple[str, Any]):
        keysCount = len(keys)
        finds = 0

        if (type(gdbMIResponse) is list):
            for r in gdbMIResponse:
                selected = self.selectResponse(r, *keys)
                if (selected is not None):
                    return selected
        elif (type(gdbMIResponse) is dict):
            for key in keys:
                if (gdbMIResponse.get(key[0]) == key[1]):
                    finds += 1

            if (finds == keysCount):
                return gdbMIResponse

        return None

class MICommands:
    MI_CONTINUE = "-exec-continue"
    MI_STEPNX = "-exec-next"
    MI_STEPIN = "-exec-step"
    MI_STEPOUT = "-exec-finish"

    MI_THREADINF = "-thread-info"

    MI_BREAKLIST = "-break-list"
    MI_BREAKADD = "-break-insert"
    MI_BREAKREM = "-break-delete"

    MIPREFIX_EXEC = "-exec"
