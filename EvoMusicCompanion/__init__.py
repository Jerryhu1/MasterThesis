import sys

from PyQt5.QtWidgets import QApplication
from math import ceil

from ea.constants import POPULATION_SIZE
from ea.simulation import Simulation, constants
import pandas as pd
from gui.Main import Main

if __name__ == '__main__':
    #pitch_matrix = pd.read_csv('piano_man.csv', index_col=0)
    #duration_matrix = pd.read_csv('piano_man_duration.csv', index_col=0)
    duration_matrix = None
    pitch_matrix = None
    crossover = ["NONE"]
    pop_sizes = [1000]
    iterations = [500]
    learning_rates = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    systems = ["MODEL"]
    selection_size = [0.1, 0.2, 0.3, 0.4, 0.5]
    constants.RUN_MODE = "MULTIPLE"
    constants.METRIC_MODE = "MULTIPLE"  # ALL
    if constants.RUN_MODE == "MULTIPLE":
        runs = 4
    else:
        runs = 1
    print("Starting all experiments")
    print(f"Mode: {constants.RUN_MODE}")
    print(f"Metric mode: {constants.METRIC_MODE}")
    for s in systems:
        constants.SYSTEM = s
        for sel in selection_size:
            constants.SELECTION_SIZE = ceil(1000 * sel)
            for i in iterations:
                constants.ITERATIONS = i
                for n in pop_sizes:
                    for r in range(runs):
                        constants.POPULATION_SIZE = n
                        constants.ELITISM_SIZE = ceil(n * 0.05)
                        constants.CROSSOVER_POPULATION = ceil(n * 0.5)
                        constants.MODEL_POPULATION = ceil(n * 0.5)
                        #constants.SELECTION_SIZE = 50
                        print("Running experiment: Selection size \n")
                        print(f"System: {s}")
                        print(f"Population size: {n}")
                        print(f"Iterations: {i}")
                        print(f"Elitism size: {constants.ELITISM_SIZE}")
                        if s == "GA" or s == "HYBRID":
                            print(f"Crossover: {c}")
                        if s == "MODEL" or s == "HYBRID":
                            print(f"Learning rate: {constants.LEARNING_RATE}")
                            print(f"Selection size: {constants.SELECTION_SIZE}")
                        if s == "HYBRID":
                            print(f"GA pop size: {constants.CROSSOVER_POPULATION}")
                            print(f"MODEL pop size: {constants.MODEL_POPULATION}")

                        sim = Simulation(duration_matrix, pitch_matrix)
                        sim.run(pitch_matrix, duration_matrix, None)

    #app = QApplication(sys.argv)
    #ex = Main()
    #sys.exit(app.exec_())
