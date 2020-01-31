import sys

from PyQt5.QtWidgets import QApplication

from ea.simulation import Simulation, constants
import pandas as pd
from gui.Main import Main

if __name__ == '__main__':
    #pitch_matrix = pd.read_csv('piano_man.csv', index_col=0)
    #duration_matrix = pd.read_csv('piano_man_duration.csv', index_col=0)
    duration_matrix = None
    pitch_matrix = None
    crossover = ["1X+2X"]
    pop_sizes = [100]
    iterations = [101]
    for x in crossover:
        constants.CROSSOVER = x
        for i in iterations:
            constants.ITERATIONS = i
            for n in pop_sizes:
                constants.POPULATION_SIZE = n
                sim = Simulation(duration_matrix, pitch_matrix)
                sim.run(pitch_matrix, duration_matrix, None)
    #app = QApplication(sys.argv)
    #ex = Main()
    #sys.exit(app.exec_())
