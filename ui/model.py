from backend import code, memory, symbols, cpu, gdbmi

class DearGDBModel:
    currentThread: int
    currentBreakpoint: str

    registers: dict
    breakpoints: list[dict]

    variables: list[dict]

    def __init__(self, gdbMI: gdbmi.GdbMI) -> None:
        self.codeMgr = code.CodeManager(gdbMI)
        self.symMgr = symbols.SymbolsManager(gdbMI)
        self.memMgr = memory.MemoryManager(gdbMI)
        self.cpuMgr = cpu.CPUManager(gdbMI)
        self.gdbMI = gdbMI

    def getThreadInfo(self):
        responses = self.cpuMgr.getThreadInfo()
        threadsResponse = self.cpuMgr.selectResponse(responses, ("token", self.cpuMgr.token()))

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
