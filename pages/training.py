import PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QGridLayout

from generate_ecg_plot import get_ecg_svg
import qtawesome as qta

class Training(QWidget):
    def __init__(self):
        super().__init__()
         
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
  
        self.button = QPushButton("I AM TRAINING PAGE")
        self.text = QLabel("Hello World")

        self.qsw = QSvgWidget()
        self.qsw.load(get_ecg_svg())
        self.qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        #self.layout.addWidget(qsw)
    
        self.setupTxtBox()

    def setupTxtBox(self):
        ##maybe Qlabel instead of Qlineedit
        self.textboxTitle = QLineEdit('You are Currently Training')
        self.textboxSubtitle = QLineEdit('Hit the space bar to proceed to the next ECG strip')
        self.textboxRhythmName = QLineEdit('Sinus Bradycardia')
        self.textboxHR = QLineEdit('Heart Rate (bpm): <60')
        self.textboxRhy = QLineEdit('Rhythm: Regular, evenly spaced')
        self.textboxPwav = QLineEdit('P-wave: Before each QRS, identical waves')
        self.textboxPRint = QLineEdit('PR Interval (seconds): 0.12 - 0.20')
        self.textboxQRScom = QLineEdit('QRS Complex (seconds): < 0.12')
        self.textboxNotes = QLineEdit('Notes: In this rhythm, the impulses originate at the SA node at a slow rate. This may be caused by increased vagal or parasympathetic tones.')

        box = QGridLayout()
        #add ECG graph widget here first
        #box.addWidget(self.get_ecg_png(), 0, 0)
        box.addWidget(self.textboxTitle, 1, 0)
        box.addWidget(self.textboxSubtitle, 2, 0)
        box.addWidget(self.qsw, 3, 0)
        box.addWidget(self.textboxRhythmName, 4, 0)
        box.addWidget(self.textboxHR, 5, 0)
        box.addWidget(self.textboxRhy, 6, 0)
        box.addWidget(self.textboxPwav, 7, 0)
        box.addWidget(self.textboxPRint, 5, 4)
        box.addWidget(self.textboxQRScom, 6, 4)
        box.addWidget(self.textboxNotes, 7, 4)

        self.setLayout(box)
