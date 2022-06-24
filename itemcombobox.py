from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox


class ItemComboBox(QComboBox):
    item_swap = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.activated.connect(self.on_changed)

    def on_changed(self, text):
        c_text = self.currentText()
        print("changed ", self.objectName(), c_text)
        self.item_swap.emit()
