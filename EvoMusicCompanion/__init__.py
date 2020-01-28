import sys

from PyQt5.QtWidgets import QApplication

from ea.simulation import Simulation
import pandas as pd
from gui.Main import Main

if __name__ == '__main__':
    #pitch_matrix = pd.read_csv('piano_man.csv', index_col=0)
    #duration_matrix = pd.read_csv('piano_man_duration.csv', index_col=0)
    duration_matrix = None
    pitch_matrix = None
    sim = Simulation(0.5, 100, duration_matrix, pitch_matrix)
    sim.run(5, pitch_matrix, duration_matrix, None)
    #app = QApplication(sys.argv)
    #ex = Main()
    #sys.exit(app.exec_())
