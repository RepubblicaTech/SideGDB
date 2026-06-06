from math import floor

from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QScrollArea

from ui.QtHelpers import Resettable
from ui.subwindows.QCodeWidgets.QSourceWidget import QSourceWidget


class QCodeArea(QScrollArea, Resettable):
    def __init__(self):
        self.firstLine = 0  # first line on screen
        self.linesOnScreen = 0

        super().__init__()

        self.sourceWidget = QSourceWidget()
        self.setWidget(self.sourceWidget)
        self.setWidgetResizable(True)

    def loadSource(self, path: str):
        self.sourceWidget.loadSource(path)

    def highlightLine(self, line: int):
        self.sourceWidget.highlightLine(line)

    def scrollTo(self, line: int):
        if (line >= self.firstLine and line <= self.firstLine + self.linesOnScreen):
            return

        firstLine = floor(line - (self.linesOnScreen / 2))
        if (firstLine < 1):
            firstLine = 1

        self.verticalScrollBar().setValue(firstLine * self.viewport().fontMetrics().height())

    def scrollContentsBy(self, dx: int, dy: int, /) -> None:
        self.firstLine = self.firstLine - round(dy / self.viewport().fontMetrics().height())
        return super().scrollContentsBy(dx, dy)

    def resizeEvent(self, e: QResizeEvent, /) -> None:
        self.linesOnScreen = floor(self.viewport().height() / self.viewport().fontMetrics().height())
        return super().resizeEvent(e)

    def sgReset(self):
        self.firstLine = 0
        self.linesOnScreen = 0

        self.sourceWidget.sgReset()
        self.update()
