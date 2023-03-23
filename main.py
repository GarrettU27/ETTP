# https://www.riverbankcomputing.com/software/pyqt/
# https://pypi.org/project/neurokit2/
# Potentially useful: https://coderslegacy.com/python/pyqt6-css-stylesheets/
import os.path

import PyQt6
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
import sys
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont("./fonts/EncodeSans.ttf")
    QFontDatabase.addApplicationFont("./fonts/EncodeSansSC.ttf")
    PyQt6.QtCore.QDir.addSearchPath('images', os.path.abspath("./images"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
