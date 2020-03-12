from math import ceil
import time
from ea.simulation import Simulation, constants
import os
import json
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Start an experiment')
    parser.add_argument('--name', metavar='name', required=True, help='Name of the experiment')
    parser.add_argument('--settings', metavar='path', required=False, help='Path to the setting.json')

    args = parser.parse_args()

    #pitch_matrix = pd.read_csv('piano_man.csv', index_col=0)
    #duration_matrix = pd.read_csv('piano_man_duration.csv', index_col=0)
    duration_matrix = None
    pitch_matrix = None

    with open("settings.json", "r") as settings:
        data = json.load(settings)
        print(data)
        constants.LEARNING_RATE = data['LEARNING_RATE']
        constants.SYSTEM = data['SYSTEM']
        constants.SELECTION_SIZE = data['SELECTION_SIZE']
        constants.RUN_MODE = "MULTIPLE"
        constants.METRIC_MODE = "MULTIPLE"  # ALL
        constants.CROSSOVER = data['CROSSOVER']
        constants.POPULATION_SIZE = data['POPULATION_SIZE']
        constants.ELITISM_SIZE = data['ELITISM_SIZE']
        constants.CROSSOVER_POPULATION = data['CROSSOVER_POPULATION']
        constants.MODEL_POPULATION = data['MODEL_POPULATION']
        constants.FILE_PREFIX = data['FILE_PREFIX']
        constants.ITERATIONS = data['ITERATIONS']
        constants.NUM_OF_MEASURES = data['MEASURES']
        constants.SUBRATER_TARGET_VALUE = data['SUBRATER_TARGET_VALUE']
        runs = data['RUNS']

    print(f"Running experiment: {args.name} \n")
    print(f"Runs: {runs} \n")
    print(f"Mode: {constants.RUN_MODE}")
    print(f"Metric mode: {constants.METRIC_MODE}")

    for r in range(runs):
        print(f"System: {constants.SYSTEM}")
        print(f"Elitism size: {constants.ELITISM_SIZE}")
        print(f"Run: {r}")
        if constants.SYSTEM == "GA" or constants.SYSTEM == "HYBRID":
            print(f"Crossover: {constants.CROSSOVER}")
        if constants.SYSTEM == "MODEL" or constants.SYSTEM == "HYBRID":
            print(f"Learning rate: {constants.LEARNING_RATE}")
            print(f"Selection size: {constants.SELECTION_SIZE}")
        if constants.SYSTEM == "HYBRID":
            print(f"GA pop size: {constants.CROSSOVER_POPULATION}")
            print(f"MODEL pop size: {constants.MODEL_POPULATION}")

        sim = Simulation(duration_matrix, pitch_matrix)
        sim.run(pitch_matrix, duration_matrix, None)

    #app = QApplication(sys.argv)
    #ex = Main()
    #sys.exit(app.exec_())
