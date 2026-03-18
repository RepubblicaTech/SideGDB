from backend.GdbMi import GdbMI, GdbMIManager

class SymbolsManager(GdbMIManager):

    def __init__(self, gdbMI: GdbMI):
        super().__init__(gdbMI)
        self.GDBMI_TOKEN = "SYM"

    def showStackVariables(self):
        return self.sendCmd("-stack-list-locals --all-values")

    def getVariableValue(self, varName: str):
        return self.sendCmd(f"-data-evaluate-expression {varName}")
