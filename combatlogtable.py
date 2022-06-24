from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class CombatLogTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setRowCount(100)
        self.setColumnCount(100)

    # data parameter = list of dictionary example: [{k:v}, {k,v} {k,v}]
    def populate_combat_log(self, data_list):
        print("UI_LOG: POPULATE COMBAT LOG")
        self.setRowCount(len(data_list))
        for item_idx, entry_dict in enumerate(data_list):
            for key_idx, key in enumerate(entry_dict):
                item_value = QTableWidgetItem(str(entry_dict[key]))
                self.setItem(item_idx, key_idx, item_value)

        self.resizeColumnsToContents()
