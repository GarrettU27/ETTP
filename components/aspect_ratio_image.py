# https://stackoverflow.com/questions/8211982/qt-resizing-a-qlabel-containing-a-qpixmap-while-keeping-its-aspect-ratio

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QLabel


class AspectRatioImage(QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1, 1)
        self.setScaledContents(False)
        self.pix = None

    def setPixmap(self, p: QtGui.QPixmap) -> None:
        self.pix = p
        QLabel.setPixmap(self, self.scaledPixmap())

    def heightForWidth(self, width: int) -> int:
        if self.pix is None:
            return self.height()
        else:
            return int((self.pix.height() * width) / max(1, self.pix.width()))

    def sizeHint(self) -> QtCore.QSize:
        w = self.width()
        return QSize(w, self.heightForWidth(w))

    def scaledPixmap(self):
        p = self.pix.scaled(self.size() * self.devicePixelRatio(), Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
        p.setDevicePixelRatio(self.devicePixelRatio())
        return p

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        super().resizeEvent(e)
        if self.pix is not None:
            QLabel.setPixmap(self, self.scaledPixmap())
