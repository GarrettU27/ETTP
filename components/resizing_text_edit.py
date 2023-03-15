# https://stackoverflow.com/questions/47710329/how-to-adjust-qtextedit-to-fit-its-contents
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6 import QtGui


class ResizingTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def sizeHint(self) -> QtCore.QSize:
        s = self.document().size().toSize()

        s.setWidth(max(100, s.width()))
        s.setHeight(max(100, s.height()))
        return s

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.updateGeometry()
        super().resizeEvent(event)