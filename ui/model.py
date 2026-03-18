from backend import code, memory, symbols, cpu, GdbMi

class SGDBModel:
    currentThread: int
    currentBreakpoint: str

    registers: dict
    breakpoints: list[dict]

    variables: list[dict]

    def __init__(self, gdbMI: GdbMi.GdbMI) -> None:
        self.__gdbMI = gdbMI

        self.__codeMgr = code.CodeManager(gdbMI)
        self.__symMgr = symbols.SymbolsManager(gdbMI)
        self.__memMgr = memory.MemoryManager(gdbMI)
        self.__cpuMgr = cpu.CPUManager(gdbMI)

    def getThreadInfo(self):
        responses = self.__cpuMgr.getThreadInfo()
        threadsResponse = self.__cpuMgr.selectResponse(responses, ("token", self.__cpuMgr.token()))

        threadsFrame: dict = {
            "current_thread": threadsResponse["payload"]["current-thread-id"],
            "threads": []
        }

        for thread in threadsResponse["payload"]["threads"]:
            threadsFrame["threads"].append({
                "id": thread["id"],
                "state": thread["state"],
                "frame": thread["frame"]
            })

        self.currentThread = threadsFrame["current_thread"]

        return threadsFrame
