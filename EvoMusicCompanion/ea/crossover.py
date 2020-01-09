from ea import fitness, initialisation
from ea.individual import Individual, Measure, Note
from random import Random
import copy

rng = Random()


def measure_crossover(p1: Individual, p2: Individual):
    # No crossover possible from first and last indices

    # one or two point crossover
    p = rng.random()
    if p > 0.5:
        c1, c2 = two_point(p1, p2)
    else:
        c1, c2 = one_point(p1, p2)

    # Set the chords correctly
    initialisation.set_chords(c1)
    initialisation.set_chords(c2)

    return c1, c2


def two_point(p1, p2):
    # one or two point crossover
    p = rng.random()
    point1 = rng.randrange(1, len(p1.measures))
    point2 = rng.randrange(1, len(p1.measures))

    while point1 == point2:
        point1 = rng.randrange(1, len(p1.measures))
        point2 = rng.randrange(1, len(p1.measures))
    if point1 > point2:
        temp = point2
        point2 = point1
        point1 = temp

    c1 = Individual([], None)
    c2 = Individual([], None)

    p1_measures = copy.deepcopy(p1.measures)
    p2_measures = copy.deepcopy(p2.measures)

    for i in range(0, point1):
        c1.measures.append(p1_measures[i])
        c2.measures.append(p2_measures[i])
    for i in range(point1, point2):
        c1.measures.append(p2_measures[i])
        c2.measures.append(p1_measures[i])
    for i in range(point2, len(p1_measures)):
        c1.measures.append(p1_measures[i])
        c2.measures.append(p2_measures[i])
    return c1, c2


def one_point(p1, p2):
    point1 = rng.randrange(1, len(p1.measures))

    c1 = Individual([], None)
    c2 = Individual([], None)
    p1_measures = copy.deepcopy(p1.measures)
    p2_measures = copy.deepcopy(p2.measures)

    for i in range(0, point1):
        c1.measures.append(p1_measures[i])
        c2.measures.append(p2_measures[i])
    for i in range(point1, len(p1_measures)):
        c1.measures.append(p2_measures[i])
        c2.measures.append(p1_measures[i])
    return c1, c2


# Measures with same chord are exchanged
def measure_exchange(p1: Individual, p2: Individual):
    idx = rng.randrange(len(p1.measures))
    m1 = p1.measures[idx]
    m2 = p2.measures[idx]
    p1.measures[idx] = m2
    p2.measures[idx] = m1

