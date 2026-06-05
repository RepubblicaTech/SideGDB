from pathlib import Path

from PySide6.QtCore import QRect
from PySide6.QtGui import QPaintEvent, QPainter, QPalette
from PySide6.QtWidgets import QWidget

from ui.helpers.QtHelpers import Resettable


class QSourceWidget(QWidget, Resettable):
    BAR_BASEW = 40
    BAR_RPADD = 10
    BAR_BPADD = 50

    def __init__(self):
        self.currentSource = ""
        self.lines: list = []
        self.lineToHighlight = 0

        super().__init__()

    @staticmethod
    def digits(n):
        d = 1
        while (n >= 10):
            n /= 10
            d += 1
        return d

    def totalLines(self):
        return len(self.lines)

    def barWidth(self):
        return self.BAR_BASEW + (self.fontMetrics().horizontalAdvance("9") * self.digits(self.totalLines())) + self.BAR_RPADD

    def barHeight(self):
        return self.BAR_BPADD + (self.fontMetrics().height() * self.totalLines())

    def loadSource(self, path: str):
        if (path == self.currentSource or not path or not Path(path).exists()):
            return

        self.currentSource = path
        f = open(path)
        self.lines = f.readlines()

        maxLineLength = 0
        for line in self.lines:
            if (len(line) > maxLineLength):
                maxLineLength = len(line)

        self.setMinimumHeight(self.barHeight())
        self.setMinimumWidth(self.barWidth() + (self.fontMetrics().horizontalAdvance("9") * maxLineLength))

        self.update()

    def highlightLine(self, line: int):
        if (line < 0 or line > self.totalLines()):
            return

        self.lineToHighlight = line
        self.update()

    def paintEvent(self, e: QPaintEvent, /) -> None:
        if (not self.currentSource):
            return

        painter = QPainter(self)

        painter.fillRect(0, 0, self.width(), self.height(), self.palette().color(QPalette.ColorRole.Base))
        barRect = QRect(0, 0, self.barWidth(), self.barHeight())
        painter.fillRect(barRect, self.palette().color(QPalette.ColorRole.AlternateBase))

        for i in range(self.totalLines()):
            painter.drawText(self.barWidth() - (self.fontMetrics().horizontalAdvance("9") * self.digits(i + 1)) - self.BAR_RPADD,
                             self.fontMetrics().height() * (i + 1),
                             str(i + 1))
            if (i + 1 == self.lineToHighlight):
                painter.fillRect(self.barWidth(),
                                 self.fontMetrics().height() * i,
                                 self.width(),
                                 self.fontMetrics().lineSpacing(),
                                 self.palette().color(QPalette.ColorRole.Accent))
            painter.drawText(self.barWidth(), self.fontMetrics().height() * (i + 1), self.lines[i])

        painter.end()
        return super().paintEvent(e)

    def sgReset(self):
        self.currentSource = ""
        self.lines.clear()
        self.lineToHighlight = 0

        self.update()
