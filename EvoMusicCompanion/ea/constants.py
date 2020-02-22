from math import ceil

NUM_OF_MEASURES = 4
N_GRAM = 'trigram'
LEARNING_RATE = 0.4
POPULATION_SIZE = 100
SELECTION_SIZE = ceil(POPULATION_SIZE * 0.05)
TOURNAMENT_SIZE = 4
ELITISM_SIZE = ceil(POPULATION_SIZE * 0.05)
ITERATIONS = 1000
CROSSOVER = "1X+2x"
SYSTEM = "HYBRID"
CROSSOVER_POPULATION = POPULATION_SIZE * 0.5
MODEL_POPULATION = POPULATION_SIZE * 0.5
RUN_MODE = "MULTIPLE"
METRIC_MODE = "POPULATION"

FILE_PREFIX = "NO_PREFIX_GIVEN"
METRIC_VALUE = -1

def flatten(l):
    return [item for sublist in l for item in sublist]


NOTE_RANGE = [
    'C4',
    'C#4',
    'D4',
    'D#4',
    'E4',
    'F4',
    'F#4',
    'G4',
    'G#4',
    'A4',
    'A#4',
    'B4',
    'C5',
    'C#5',
    'D5',
    'D#5',
    'E5',
    'F5',
    'F#5',
    'G5',
    'G#5',
    'A5',
    'A#5',
    'B5',
    'C6',
]

C_MAJOR_SCALE = [
    'C4',
    'D4',
    'E4',
    'F4',
    'G4',
    'A4',
    'B4',
    'C5',
    'D5',
    'E5',
    'F5',
    'G5',
    'A5',
    'B5',
    'C6',
]



DURATION_BLOCKS = [
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.5],
    [0.25, 0.75],
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.25, 0.25]
]

Wp = 0.1
Wm = 0.1
Wn = 0.5

USER_RATINGS = [
    "Very good",
    "Good",
    "Neutral",
    "Bad",
    "Very bad"
]