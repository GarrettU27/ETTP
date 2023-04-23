from typing import List

import PyQt6
import qtawesome
from PyQt6 import QtGui
from PyQt6.QtCore import QSize, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, Qt, pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QGridLayout, QToolButton, QScrollArea, QSizePolicy, QFrame, QLabel


from backend.get_ecg_from_db import Question
from components.heading_label import HeadingLabel
from components.main_button import MainButton
from components.paragraph_label import ParagraphLabel
from pages import buffer


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("""QToolButton { border: none; 
                                                        font: 32px;               
                                                    }""")
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QFrame.NoFrame)

        lay = QGridLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            Qt.DownArrow if not checked else Qt.RightArrow
        )
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward
            if not checked
            else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay

        layout.setSpacing(30)
        layout.setHorizontalSpacing(60)
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)
class TestingResults(QWidget):
    answer_labels: List[ParagraphLabel] = []
    note_labels: List[ParagraphLabel] = []
    icons: List[qtawesome.IconWidget] = []

    def __init__(self, set_state):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)

        self.heading = HeadingLabel("Test")
        self.subheading = ParagraphLabel("See what you need to study next")
        self.score = ParagraphLabel("Your total score: ", 30)

        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.subheading)
        self.layout.addWidget(self.score)

        self.grid = QGridLayout()
        self.grid.setSpacing(30)
        self.grid.setHorizontalSpacing(60)
        self.layout.addLayout(self.grid)

        new_test_button = MainButton("Start new test")
        new_test_button.clicked.connect(set_state)
        self.layout.addWidget(new_test_button)

        self.layout.addSpacerItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                              PyQt6.QtWidgets.QSizePolicy.Policy.Expanding))

    def update_page(self, answers, questions: List[Question]):
        self.clear_page()

        # This can move items closer together if needed
        # self.grid.addItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
        #                               PyQt6.QtWidgets.QSizePolicy.Policy.Fixed), 0, 3)

        number_correct = 0

        for i, (answer, question) in enumerate(zip(answers, questions)):
            answer_label = ParagraphLabel(f"{i + 1}. {answer}", 40)
            answer_label.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                       PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)
            self.setStyleSheet("""
            QLabel {
                font-family: "Encode Sans";
                font-weight: 400;
                line-height: 150%;
                height: auto;
                padding: {0.4 * self.font_size}px;
            }
                            """)            
            self.answer_labels.append(answer_label)

            if answer == question.correct_answer:
                number_correct += 1
                self.grid.addWidget(answer_label, i, 0)

                check_widget = qtawesome.IconWidget()
                check_icon = qtawesome.icon("fa5s.check", color='green')
                check_widget.setIcon(check_icon)
                check_widget.setIconSize(QSize(40, 40))
                check_widget.update()
                self.grid.addWidget(check_widget, i, 1)

                self.icons.append(check_widget)
            else:
                self.grid.addWidget(answer_label, i, 0)

                x_widget = qtawesome.IconWidget()
                x_icon = qtawesome.icon("fa5s.times", color='red')
                x_widget.setIcon(x_icon)
                x_widget.setIconSize(QSize(40, 40))
                x_widget.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Fixed,
                                       PyQt6.QtWidgets.QSizePolicy.Policy.Fixed)
                x_widget.update()
                self.grid.addWidget(x_widget, i, 1)

                self.icons.append(x_widget)

                note_label = ParagraphLabel(f"Correct answer: {question.correct_answer}", 40)
                note_label.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                         PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)
                self.note_labels.append(note_label)
                self.grid.addWidget(note_label, i, 2)

        self.score.setText(f"Your total score: {number_correct}/{len(questions)}")
        self.update_buttons_font_size()
    
    
    def updatePage(self, answers, questions: List[Question]):
        self.clear_page()
        number_correct = 0
        #Get what arrhythmia were tested on this version of the test
        arrhythmia_tested = []
        #Stores the collapsible box objects
        collapsibleboxes = []
        #Stores the layout widgets for each collapsible box
        internals = []
        #keep track of each object's count of internal widgets
        entries = []
        #Count each arrhythmia and give back the score the user got on a per arrhythmia basis
        arrhythmia_correct = []
        arrhythmia_freq = []

        #Iterate through the questions and answers
        for i, (answer, question) in enumerate(zip(answers, questions)):

            #Prepares an answer label that will be displayed on the left side of the screen showing what the user entered
            answer_label = ParagraphLabel(f"{i + 1}. {answer}", 40)
            answer_label.setMaximumHeight(30)
            answer_label.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                       PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)
            answer_label.setStyleSheet("""
            QLabel {
                font-family: "Encode Sans";
                font-weight: 400;
                line-height: 150%;
                height: auto;
                margin-right: 15px;
                margin-top: 30px;
                margin-bottom: 30px;
            }
                            """)
            #If it's the first run, then skip the if statement otherwise it will error
            if len(arrhythmia_tested) == 0:
                #adds arrhythmia to list so it will not have another collapsible box created corresponding to that arrhythmia
                arrhythmia_tested.append(question.correct_answer)
                #create the collapsible box layout and format it correctly
                box = CollapsibleBox(str(question.correct_answer))
                lay = QGridLayout()
                #lay.setContentsMargins(0,0,0,0)
                #lay.setSpacing(30)
                #lay.setHorizontalSpacing(60)
                lay.update()

                #add the corresponding objects and values to their corresponding lists, 
                collapsibleboxes.append(box)
                internals.append(lay)
                entries.append(0)
                arrhythmia_freq.append(0)
                arrhythmia_correct.append(0)

            #Check to see if the arrhythmia object should be added onto an existing object or not.
            else:
                exists = False    
                for i in range(len(arrhythmia_tested)):
                    if question.correct_answer == arrhythmia_tested[i]:
                        exists = True
                if exists == False:
                        arrhythmia_tested.append(question.correct_answer)
                        box = CollapsibleBox(str(question.correct_answer))
                        lay = QGridLayout()
                        lay.setSpacing(30)
                        lay.setHorizontalSpacing(60)
                        collapsibleboxes.append(box)
                        internals.append(lay)
                        entries.append(0)
                        arrhythmia_freq.append(0)
                        arrhythmia_correct.append(0)

            #Run if the user answered correctly            
            if answer == question.correct_answer:
                number_correct+=1
                #Search for the corresponding arrhythmia in the list of arrythmia tested
                for i in range(len(arrhythmia_tested)):
                    if(arrhythmia_tested[i] == question.correct_answer):
                        #add the answer_label to a global list and add the widget to the collapsible box layout

                        self.answer_labels.append(answer_label)
                        internals[i].addWidget(answer_label,entries[i],0)
                        #Create and add a check widget to the collapsible box layout
                        check_widget = qtawesome.IconWidget()
                        check_icon = qtawesome.icon("fa5s.check", color='green')
                        check_widget.setIcon(check_icon)
                        check_widget.setIconSize(QSize(40, 40))
                        check_widget.update()
                        internals[i].addWidget(check_widget,entries[i],1)
                        self.icons.append(check_widget)
                        note_label = ParagraphLabel(" ",20)
                        note_label.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)
                        note_label.setMaximumHeight(30)
                        self.note_labels.append(note_label)
                        internals[i].addWidget(note_label, entries[i], 2)
                        #Increment the corresponding values for each arrythmia
                        entries[i]+=1
                        arrhythmia_correct[i]+=1
                        arrhythmia_freq[i]+=1
                        

            else:
                for i in range(len(arrhythmia_tested)):
                    if(arrhythmia_tested[i] == question.correct_answer):
                        #Add answer label to layout of collapsible box
                        self.answer_labels.append(answer_label)
                        internals[i].addWidget(answer_label, entries[i], 0)

                        #Add an X icon to the layout to signify user got a question incorrect
                        x_widget = qtawesome.IconWidget()
                        x_icon = qtawesome.icon("fa5s.times", color='red')
                        x_widget.setIcon(x_icon)
                        x_widget.setIconSize(QSize(40, 40))
                        x_widget.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Fixed,
                                       PyQt6.QtWidgets.QSizePolicy.Policy.Fixed)
                        x_widget.update()
                        internals[i].addWidget(x_widget, entries[i], 1)
                        self.icons.append(x_widget)
                        #Create a label that is at the right side of the screen with the corect arrhythmia for that question
                        note_label = ParagraphLabel(f"Correct answer: {question.correct_answer}", 20)
                        note_label.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                         PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)
                        note_label.setMaximumHeight(30)
                        self.note_labels.append(note_label)
                        internals[i].addWidget(note_label, entries[i], 2)
                        #Update corresponding values for each arrhythmia
                        entries[i]+=1
                        arrhythmia_freq[i]+=1

        for i in range(len(arrhythmia_tested)):
            box = CollapsibleBox(str(arrhythmia_tested[i] + ": "+str(arrhythmia_correct[i])+"/"+str(arrhythmia_freq[i])))
            #internals[i].
            box.setContentLayout(internals[i])
            self.grid.addWidget(box,i,0) 
        self.update_buttons_font_size()
        self.score.setText(f"Your total score: {number_correct}/{len(questions)}")



    def updatePage3(self):
        content = QWidget()
        #vlay = QVBoxLayout(content)
        for i in range(10):
            box = CollapsibleBox("Collapsible Box Header-{}".format(i))
            self.grid.addWidget(box,i,0)
            lay = QVBoxLayout()
            for j in range(8):
                label = QLabel("{}".format(j))
                label.setStyleSheet(
                "background-color: {}; color : white;"
                )
                label.setAlignment(Qt.AlignCenter)
                lay.addWidget(label)

            box.setContentLayout(lay)
        #vlay.addStretch()
        #self.layout.addWidget(vlay)
    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        self.update_buttons_font_size()

    def update_buttons_font_size(self):
        button_font_size = 20

        # Magic size I measured again
        if self.width() <= 1380:
            button_font_size = 20
            self.grid.setSpacing(15)
            self.grid.setHorizontalSpacing(30)
        else:
            self.grid.setSpacing(30)
            self.grid.setHorizontalSpacing(60)

        for answer_label in self.answer_labels:
            answer_label.set_font_size(button_font_size)

        for note_label in self.note_labels:
            note_label.set_font_size(button_font_size)

        for icon in self.icons:
            icon.setIconSize(QSize(button_font_size, button_font_size))
            icon.update()

    def clear_page(self):

        # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt

        # Too lazy am I? Too Bad!
        for i in reversed(range(self.grid.count())):
            widget_to_remove = self.grid.itemAt(i).widget()
            # remove it from the layout list
            self.grid.removeWidget(widget_to_remove)
            # remove it from the gui
            widget_to_remove.setParent(None)
