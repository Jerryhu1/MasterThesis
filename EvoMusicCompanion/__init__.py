from math import ceil
import time
from ea.simulation import Simulation, constants
import os


if __name__ == '__main__':
    #pitch_matrix = pd.read_csv('piano_man.csv', index_col=0)
    #duration_matrix = pd.read_csv('piano_man_duration.csv', index_col=0)
    duration_matrix = None
    pitch_matrix = None

    constants.LEARNING_RATE = float(os.environ.get('LEARNING_RATE'))
    constants.SYSTEM = os.environ.get('SYSTEM')
    constants.SELECTION_SIZE = int(os.environ.get('SELECTION_SIZE'))
    constants.RUN_MODE = "MULTIPLE"
    constants.METRIC_MODE = "MULTIPLE"  # ALL
    constants.CROSSOVER = os.environ.get('CROSSOVER')
    constants.POPULATION_SIZE = int(os.environ.get('POPULATION_SIZE'))
    constants.ELITISM_SIZE = int(os.environ.get('ELITISM_SIZE'))
    constants.CROSSOVER_POPULATION = int(os.environ.get('CROSSOVER_POPULATION'))
    constants.MODEL_POPULATION = int(os.environ.get('MODEL_POPULATION'))
    constants.FILE_PREFIX = os.environ.get('FILE_PREFIX')
    constants.METRIC_VALUE = os.environ.get('METRIC_VALUE')
    constants.ITERATIONS = int(os.environ.get('ITERATIONS'))

    runs = int(os.environ.get('RUNS'))

    print("Running experiment: GA 1X+2X 15 runs \n")
    print(f"Mode: {constants.RUN_MODE}")
    print(f"Metric mode: {constants.METRIC_MODE}")

    for r in range(runs):
        start = time.time()
        print(f"System: {constants.SYSTEM}")
        print(f"Elitism size: {constants.ELITISM_SIZE}")
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
        end = time.time()
        print(f'Single run time: {end - start}')

    #app = QApplication(sys.argv)
    #ex = Main()
    #sys.exit(app.exec_())
