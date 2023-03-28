# https://stackoverflow.com/questions/8211982/qt-resizing-a-qlabel-containing-a-qpixmap-while-keeping-its-aspect-ratio

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QWidget


class ImageWidget(QWidget):
    def __init__(self, align_left=False):
        super().__init__()
        self.setMinimumSize(1, 1)
        self.pix = None
        self.align_left = align_left

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)

        # https://stackoverflow.com/questions/32032379/painting-qpixmap-in-the-center-of-qtableview-cell
        scaled_pixmap = self.scaledPixmap()

        if scaled_pixmap is not None:
            width = int(scaled_pixmap.rect().width() / self.devicePixelRatio())
            height = int(scaled_pixmap.rect().height() / self.devicePixelRatio())

            x = int(self.rect().center().x() - width / 2)
            y = int(self.rect().center().y() - height / 2)

            if self.align_left:
                painter.drawPixmap(QRect(0, 0, width, height),
                                   scaled_pixmap)
            else:
                painter.drawPixmap(QRect(x, y, width, height),
                                   scaled_pixmap)

    def setPixmap(self, p: QtGui.QPixmap) -> None:
        self.pix = p

    def heightForWidth(self, width: int) -> int:
        if self.pix is None:
            return self.height()
        else:
            return int((self.pix.height() * width) / max(1, self.pix.width()))

    def sizeHint(self) -> QtCore.QSize:
        w = self.width()
        return QSize(w, self.heightForWidth(w))

    def scaledPixmap(self) -> QPixmap | None:
        if self.pix is not None:
            p = self.pix.scaled(self.size() * self.devicePixelRatio(), Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation)
            p.setDevicePixelRatio(self.devicePixelRatio())
            return p
        else:
            return None
