import PyQt6
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

from components.heading_label import HeadingLabel
from components.image_widget import ImageWidget
from components.resizing_text_edit import ResizingTextEdit


class LeadPlacement(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(HeadingLabel("Where are the 12 Leads Placed on the Body"))

        layout2 = QHBoxLayout()
        self.lead_placement_explanation = ResizingTextEdit()
        self.lead_placement_explanation.setReadOnly(True)

        self.lead_placement_explanation.setStyleSheet("""
            * {
                font-family: "Encode Sans";
                font-weight: 400;
                line-height: 150%;
                font-size: 20px;
                height: auto;
                border: none;
            }
        """)

        self.lead_placement_explanation.setHtml("""
        <p>Each of the 12 leads represent a particular orientation in space:</p>

        <ul>
            <li>Bipolar (standard) limb leads on the frontal plane</li>
            <ul>
                <li>Lead I</li>
                <ul>
                    <li>RA (-) to LA (=)</li>
                </ul>
        
                <li>Lead II</li>
                <ul>
                    <li>RA (-) to LF (+)</li>
                </ul>
        
                <li>Lead III</li>
                <ul>
                    <li>LA (-) to LF (+)</li>
                </ul>
            </ul>
        
            <li>Augmented Unipolar limb leads on the frontal plane</li>
            <ul>
                <li>Lead aVR</li>
                <ul>
                    <li>RA (-) to (LA & LF) (+)</li>
                </ul>
        
                <li>Lead aVL</li>
                <ul>
                    <li>LA (+) to (RA & LF) (-)</li>
                </ul>
        
                <li>Lead aVF</li>
                <ul>
                    <li>LF (+) to (LA & RA) (-)</li>
                </ul>
            </ul>
        
            <li>Unipolar (+) chest leads on the horizontal plane</li>
            <ul>
                <li>Posterior, Anterior</li>
                <ul>
                    <li>Lead V1</li>
                    <li>Lead V2</li>
                    <li>Lead V3</li>
                </ul>
        
                <li>Right, Left</li>
                <ul>
                    <li>Lead V4</li>
                    <li>Lead V5</li>
                    <li>Lead V6</li>
                </ul>
            </ul>
        </ul>
        """)

        self.layout.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)

        image = ImageWidget(True)
        pixmap = QPixmap('images:lead_placement.png')
        image.setPixmap(pixmap)
        image.setMaximumHeight(800)

        layout2.addWidget(self.lead_placement_explanation)
        layout2.addWidget(image)
        layout2.setAlignment(image, PyQt6.QtCore.Qt.AlignmentFlag.AlignTop)

        layout2.setStretch(0, 1)
        layout2.setStretch(1, 1)

        self.layout.addLayout(layout2)
