from PyQt6.QtWidgets import QTreeWidgetItem


class BurgerItem(QTreeWidgetItem):
    def __init__(self, column_names, index: int):
        super().__init__(column_names)
        self.index = index
