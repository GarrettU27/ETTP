import PyQt6
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QSpacerItem, QLabel, QVBoxLayout, QHBoxLayout

from components.heading_label import HeadingLabel
from components.image_widget import ImageWidget
from components.resizing_text_edit import ResizingTextEdit
from components.arrythmia_picture import ArrythmiaPicture
from components.paragraph_label import ParagraphLabel

class ReadECG(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(HeadingLabel("How do I read a 12-lead ECG?"))

        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()
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
            it represents 0.5 mV. Five large squares represent 1 second, and there are 300 large quares per minute.</p>
        <br>
        <p><strong>Calculating Heart Rate:</strong> There are a few different ways to calculate the heart rate on an ECG strip, with the assumption that the paper is running at the regular standard speed of 25mm/second. 
            <li>1) Count the number of large squares between each R wave, and divde 300 by that number. </li>
            <li>2) Count the number of small squares between each R wave, and divde 1,500 by that number. </li>
        <br>
        <p> Sources:</p>
            <li>1) Chatterjee, S. and Miller, A. "Biomedical Instrumentation Systems." Delmar, Cengage Learning. 2010.</li>
            <li>2) Malminvuo, J. and Plonsey, R. "Bioelectromagnetism - Principles and Applications of Bioelectric and Biomagnetic Fields." Oxford University Press. 1995.</li>
            <li>3) Meek, S. and Morris, F. "ABC of clinical electrocaridography: Introduction. I-Leads, rate, rhythm, and cardiac axis." BMJ Clinical Review. Vol 324: 415-8. 16FEB2002.<li>
            <li>4) Webster, John. 	"Medical Instrumentation, Application and Design," Fourth Edition. Wiley 2010.</li>
        """)     

        ##start Sources list
        #self.sources = ResizingTextEdit()
        #self.sources.setReadOnly(True)
        #self.sources.setStyleSheet("""
         #   * {
         #       font-family: "Encode Sans";
         #       font-weight: 400;
         #       line-height: 150%;
         #       font-size: 20px;
         #       height: auto;
         #       border: none;
         #   }
        #""")
        #self.sources.setHtml("""
        #<p> Sources:</p>
        #    <li>1) Chatterjee, S. and Miller, A. "Biomedical Instrumentation Systems." Delmar, Cengage Learning. 2010.</li>
        #    <li>2) Malminvuo, J. and Plonsey, R. "Bioelectromagnetism - Principles and Applications of Bioelectric and Biomagnetic Fields." Oxford University Press. 1995.</li>
        #    <li>3) Meek, S. and Morris, F. "ABC of clinical electrocaridography: Introduction. I-Leads, rate, rhythm, and cardiac axis." BMJ Clinical Review. Vol 324: 415-8. 16FEB2002.<li>
        #    <li>4) Webster, John. 	"Medical Instrumentation, Application and Design," Fourth Edition. Wiley 2010.</li>
        #""")

        #self.sources = ResizingTextEdit()
        #self.sources.setReadOnly(True)

        #layout3.addWidget(self.image)
        #layout3.setAlignment(self.image, PyQt6.QtCore.Qt.AlignmentFlag.AlignBottom)
        #layout3.addWidget(self.sources)
        ##End Sources List

        #Start Layout
        self.image = ImageWidget(True)
        self.pixmap = QPixmap("images:read_ecg.png")
        self.image.setPixmap(self.pixmap)
        self.image.setMaximumHeight(800)

        layout2.addWidget(self.image)
        layout2.setAlignment(self.image, PyQt6.QtCore.Qt.AlignmentFlag.AlignTop)
        layout2.addWidget(self.read_ecg_explanation)

        self.image2 = ImageWidget(True)
        self.pixmap = QPixmap("images:HeartRates.png")
        self.image2.setPixmap(self.pixmap)
        self.image2.setMaximumHeight(1000)

        layout2.addWidget(self.image2)
        layout2.setAlignment(self.image2, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        #layout2.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        layout2.setSpacing(50)

        layout2.setStretch(0, 1)
        layout2.setStretch(1, 1)

        self.layout.addLayout(layout2)

        ##Heart rate image placement after 1stblock of text
        #self.image2 = ImageWidget(True)
       # self.pixmap = QPixmap("images:HeartRates.png")
       # self.image2.setPixmap(self.pixmap)
       # self.image2.setMaximumHeight(1000)

        #layout3.addWidget(self.image2)
        #layout3.setAlignment(self.image2, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        #layout3.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        #layout3.setSpacing(50)

        #self.layout.addLayout(layout3)

        #start Arrythmia Examples Set up
       # layout4 = QHBoxLayout()    
        #self.layout4 = QVBoxLayout(self)
       # self.layout4.setSpacing(16)

        rythms = [
            ("", "<strong>Next we will look at a sampling of ideal arrythmia waveforms. Training mode will provide you with more details about each arrythmia, but this will give you a good place to start</strong>"),
            ("images:NormalSinusRhythm.png", "Normal Sinus Rhythm: heart rate of 60-100 bpm, PR interval is 0.12-0.20 seconds, and QRS complex < 0.12 seconds"),
            ("images:NormalSinusRhythm2.png", "A second example of normal sinus rhythm."),
            ("images:SinusTachycardia.png", "Sinus Tachycardia: elevated heart rate greater than 100 bpm."),
            ("images:SinusTachycardia2.png", "A second example of sinus tachcardia."),
            ("images:SinusBradycardia.png", "Sinus Bradycardia: slow heart rate less than 60 bpm."),
            ("images:SinusBradycardia2.png", "A second example of sinus bradycardia."), 
            ("images:AtrialFibrillation.jpg", "Atrial Fibrillation: rapid atrial rate, slow ventricular rate, with rapid and irregular p-wave and rhythm."),
            ("images:AtrialFlutter.png", "Atrial Flutter: heart rate of 220-300 bpm with a sawtoothed p wave."),
            ("images:FirstDegreeAVBlock.png", "1st Degree AV Block: lengthened PR interval greater than 0.2 seconds."),
            ("images:SecondDegreeAVBlock.png", "2nd Degree AV Block: longest PR interval just before QRS wave is dropped."), 
            ("images:ThirdDegreeAVBlock.png", "3rd Degree AV Block: p wave is regular but out of sync with QRS."), 
            ("", "ECG Examples Source: Chatterjee, S. and Miller, A. Biomedical Instrumentation Systems. Delmar, Cengage Learning. 2010."),
        ]
        ##end arrythmia examples set up

        #example Arrythmia layout
        for image, name, in rythms:
            horizontal_layout3 = QHBoxLayout()
            horizontal_layout3.setSpacing(30)
            horizontal_layout3.addWidget(ArrythmiaPicture(image))
            horizontal_layout3.addWidget(ParagraphLabel(name))
            self.layout.addLayout(horizontal_layout3)

        self.layout.addSpacerItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                          PyQt6.QtWidgets.QSizePolicy.Policy.Expanding))
        self.layout.addLayout(layout3)