from ea import fitness, initialisation
from ea.individual import Individual, Measure, Note
from random import Random

rng = Random()


def measure_crossover(p1: Individual, p2: Individual):
    # No crossover possible from first and last indices
    point1 = rng.randrange(1, len(p1.measures))
    point2 = rng.randrange(1, len(p1.measures))

    c1 = Individual([], None)
    c2 = Individual([], None)

    for i in range(0, point1):
        c1.measures.append(p1.measures[i])
        c2.measures.append(p2.measures[i])

    for i in range(point1, 4):
        c1.measures.append(p2.measures[i])
        c2.measures.append(p1.measures[i])
    # Set the chords correctly
    initialisation.set_chords(c1)
    initialisation.set_chords(c2)

    return c1, c2


# Measures with same chord are exchanged
def measure_exchange(p1: Individual, p2: Individual):
    idx = rng.randrange(len(p1.measures))
    m1 = p1.measures[idx]
    m2 = p2.measures[idx]
    p1.measures[idx] = m2
    p2.measures[idx] = m1

