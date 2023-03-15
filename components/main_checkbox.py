from components.main_button import MainButton


class MainCheckbox(MainButton):
    def __init__(self, text):
        super().__init__(text)

        self.setChecked(False)
        self.setCheckable(True)
        self.clicked.connect(self.selected)

    def selected(self):
        if self.isChecked():
            self.setStyleSheet("""
                QPushButton {
                    font-family: "Encode Sans";
                    font-weight: 400;
                    font-size: 40px;
                    line-height: 150%;
                    text-align: center;
                    color: #FFFFFF;
                    background: #44AF69;
                    padding: 0.4em;
                    border-radius: 25%;
                    margin-bottom: 30px;
                }

                QPushButton:hover {
                    background: #368c54;
                }
            """)
        else:
            self.set_main_button_style()