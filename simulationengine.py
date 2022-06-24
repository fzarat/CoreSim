from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

import Warrior as warr


class SimulationEngine(QWidget):
    sim_complete = pyqtSignal()
    my_warr = warr.Warrior()

    def __init__(self, parent):
        super().__init__(parent)

    def run_sim(self):
        self.my_warr.initialize_env()

        global testdata
        testdata = self.my_warr.combat_log
        self.sim_complete.emit()
