from PyQt6.QtWidgets import QTreeWidgetItem, QWidget


class BurgerItem(QTreeWidgetItem):
    def __init__(self, column_names, widget: QWidget):
        super().__init__(column_names)
        self.widget = widget
