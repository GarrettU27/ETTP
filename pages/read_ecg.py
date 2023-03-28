import PyQt6
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

from components.heading_label import HeadingLabel
from components.image_widget import ImageWidget
from components.resizing_text_edit import ResizingTextEdit


class ReadECG(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(HeadingLabel("How do I read a 12-lead ECG?"))

        layout2 = QHBoxLayout()
        self.read_ecg_explanation = ResizingTextEdit()
        self.read_ecg_explanation.setReadOnly(True)

        self.read_ecg_explanation.setStyleSheet("""
            * {
                font-family: "Encode Sans";
                font-weight: 400;
                line-height: 150%;
                font-size: 20px;
                height: auto;
                border: none;
            }
        """)

        self.read_ecg_explanation.setHtml("""
        <p><strong>P-wave:</strong> Atrial depolarization. The width of the P-wave reflects 
            the spread of depolarization over the atria</p>
        <p><strong>PR Interval:</strong> AV, or atrioventricular, conduction. This is the depolarization from 
            the SA node, or sinoatrial node, propogates through the AV node, AV bundle, bundle 
            branches, and the Purkinje network</p>
        <p><strong>QRS Complex:</strong> Ventricular depolarization, or activation, wave. Illustrates the electrical impulse
            as it spreads through the ventricles.</p>
        <p><strong>ST Segment:</strong> The plateau of the ventricular action potential. The membrane potential is relatively 
            unchanged during this time </p>
        <p><strong>T-wave:</strong> Ventricular repolarization, or recovery,  wave.  This occurs in the lower chambers of the heart, after a
             contraction, or heartbeat. It represents the repolarization of the ventricular myocardium</p>
        <p><strong>Small Squares:</strong> These are usually 1mm square. Horizontally they represent 0.04 
            seconds, and vertically they represent 0.1 mV.</p>
        <p><strong>Large Squares:</strong> These are made up of 25 little squares, 5mm square. Horizontally it represents 0.2 seconds, and vertically 
            it represents 0.5 mV.</p>
        """)

        self.image = ImageWidget(True)
        self.pixmap = QPixmap("images:read_ecg.png")
        self.image.setPixmap(self.pixmap)
        self.image.setMaximumHeight(800)

        layout2.addWidget(self.image)
        layout2.setAlignment(self.image, PyQt6.QtCore.Qt.AlignmentFlag.AlignTop)
        layout2.addWidget(self.read_ecg_explanation)

        layout2.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignTop)
        layout2.setSpacing(50)

        layout2.setStretch(0, 1)
        layout2.setStretch(1, 1)

        self.layout.addLayout(layout2)
