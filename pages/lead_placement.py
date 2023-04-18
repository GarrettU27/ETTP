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
        self.layout.addWidget(HeadingLabel("Where are the 12 Leads Placed on the Body?"))

        layout2 = QHBoxLayout()
        #layout3 = QHBoxLayout()
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
        <p>Each of the 12 leads represent a particular orientation in space around the heart:</p>

        <ul>
            <li>Bipolar (standard) limb leads on the frontal plane</li>
            <ul>
                <li>Lead I</li>
                <ul>
                    <li>RA (-) to LA (+)</li>
                </ul>
        
                <li>Lead II</li>
                <ul>
                    <li>RA (-) to LL (+)</li>
                </ul>
        
                <li>Lead III</li>
                <ul>
                    <li>LA (-) to LL (+)</li>
                </ul>
            </ul>
        
            <li>Augmented Unipolar limb leads* on the frontal plane</li>
            <ul>
                <li>Lead aVR</li>
                <ul>
                    <li>RA (-) to (LA & LL) (+)</li>
                </ul>
        
                <li>Lead aVL</li>
                <ul>
                    <li>LA (+) to (RA & LL) (-)</li>
                </ul>
        
                <li>Lead aVF</li>
                <ul>
                    <li>LL (+) to (LA & RA) (-)</li>
                </ul>
            </ul>  
        
            <li>Unipolar (+) chest leads** on the horizontal plane</li>
            <ul>
                <li>Posterior, Anterior</li>
                <ul>
                    <li>Lead V1: placed at the 4th intercoastal space at the R sternal boarder</li>
                    <li>Lead V2: placed at the 4th intercoastal space at the L sternal boarder</li>
                    <li>Lead V3: placed at the space between Leads V2 and V4</li>
                </ul>
        
                <li>Right, Left</li>
                <ul>
                    <li>Lead V4: placed at the 5th L intercoastal space in the midclavicular line</li>
                    <li>Lead V5: placed horizontally even with lead V4 but in the anterior axillary line</li>
                    <li>Lead V6: placed horzontally even with leads V4 and V5 in the midaxillary*** line.</li>
                </ul>
            </ul>

            <br>
            <li> Another way to relate these different perspectives together is to look at how they relate anatomically:</li>
            <ul>
                <li>Leads II, III, and aVF relate to the inferior surface of the heart.</li>
                <li>Leads V1 and V4 relate to the anterior surface of the heart.</li>
                <li>Leads I, aVL, V5, and V6 relate to the lateral surface of the heart.</li>
                <li>Leads V1, and aVR relate to the right atrium and the cavity of the left ventricle of the heart.</li>
                </ul>
            </ul>

            <br>
            <li>*Limb leads are said to "view" the heart along the vertical plane of the chest</li>
            <li>**Chest leads are said to "view" the heart along the horizontal plane of the chest</li>
            <li>***Midaxillary line is defined as the imaginary line that extends down from the middle of the armpit</li>
            </ul>

            <br>
            <li> Sources:</li>
            <li>1) Chatterjee, S. and Miller, A. "Biomedical Instrumentation Systems." Delmar, Cengage Learning. 2010.</li>
            <li>2) Malminvuo, J. and Plonsey, R. "Bioelectromagnetism - Principles and Applications of Bioelectric and Biomagnetic Fields." Oxford University Press. 1995.</li>
            <li>3) Meek, S. and Morris, F. "ABC of clinical electrocaridography: Introduction. I-Leads, rate, rhythm, and cardiac axis." BMJ Clinical Review. Vol 324: 415-8. 16FEB2002.<li>
            <li>4) Madhero88, ECGcolor.svg, 2009, Retrieved from: https://commons.wikimedia.org/wiki/File:ECGcolor.svg. On April 11, 2023.<li>
            </ul>
        </ul>
        """)

        self.layout.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignTop)
        image = ImageWidget(True)
        pixmap = QPixmap('images:lead_placement.png')
        image.setPixmap(pixmap)
        image.setMaximumHeight(500)

        self.layout.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)
        image2 = ImageWidget(True)
        pixmap2 = QPixmap('images:Annoatated_ECGcolor.png')
        image2.setPixmap(pixmap2)
        image2.setMaximumHeight(500)

        #layout3.addWidget(self.lead_placement_explanation)
        layout2.addWidget(image2)
        layout2.setAlignment(image2, PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)
        layout2.setSpacing(50)
        layout2.setStretch(0, 1)
        layout2.setStretch(1, 1)

        self.layout.addLayout(layout2)
        layout2.addWidget(self.lead_placement_explanation)
        layout2.addWidget(image)
        layout2.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        layout2.setSpacing(50)

        layout2.setStretch(0, 1)
        layout2.setStretch(1, 1)

        self.layout.addLayout(layout2)
