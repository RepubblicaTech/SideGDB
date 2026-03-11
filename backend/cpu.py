from backend.gdbmi import GdbMI, GdbMIManager

class CPUManager(GdbMIManager):

    def __init__(self, gdbMI: GdbMI):
        super().__init__(gdbMI)
        self.GDBMI_TOKEN = "CPU"

    def getThreadInfo(self):
        return self.sendCmd("-thread-info")

    def getRegisterNames(self):
        return self.sendCmd("-data-list-register-names")

    def getRegisterValues(self):
        return self.sendCmd("-data-list-register-values x")

    def showUpdatedRegisters(self):
        return self.sendCmd("-data-list-changed-registers")
