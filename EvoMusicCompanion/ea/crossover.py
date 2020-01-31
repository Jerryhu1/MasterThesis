import copy
from random import Random

from ea import initialisation, constants
from ea.individual import Individual

rng = Random()


def measure_crossover(p1: Individual, p2: Individual):
    # No crossover possible from first and last indices
    if constants.CROSSOVER == "UX":
        c1, c2 = uniform(p1, p2)
   # one or two point crossover
    else:
        p = rng.random()
        if constants.NUM_OF_MEASURES > 2:
            if p > 0.5:
                c1, c2 = two_point(p1, p2)
            else:
                c1, c2 = one_point(p1, p2)
        else:
            c1, c2 = one_point(p1, p2)


    # Set the chords correctly
    #initialisation.set_chords(c1)
    #initialisation.set_chords(c2)

    return c1, c2


def two_point(p1, p2):
    # one or two point crossover
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

    p1_copy = copy.deepcopy(p1)
    p2_copy = copy.deepcopy(p2)

    for i in range(0, point1):
        c1.measures.append(p1_copy.measures[i])
        c2.measures.append(p2_copy.measures[i])
    for i in range(point1, point2):
        c1.measures.append(p2_copy.measures[i])
        c2.measures.append(p1_copy.measures[i])
    for i in range(point2, len(p1_copy.measures)):
        c1.measures.append(p1_copy.measures[i])
        c2.measures.append(p2_copy.measures[i])

    if c1.measures[0] is p1.measures[0]:
        print("Child measure has reference to parent measure")
    return c1, c2


def one_point(p1, p2):
    if constants.NUM_OF_MEASURES == 2:
        point1 = 1
    else:
        point1 = rng.randrange(1, len(p1.measures))

    c1 = Individual([], None)
    c2 = Individual([], None)
    p1_copy = copy.deepcopy(p1)
    p2_copy = copy.deepcopy(p2)

    for i in range(0, point1):
        c1.measures.append(p1_copy.measures[i])
        c2.measures.append(p2_copy.measures[i])
    for i in range(point1, len(p1_copy.measures)):
        c1.measures.append(p2_copy.measures[i])
        c2.measures.append(p1_copy.measures[i])

    if c1.measures[0] is p1.measures[0] or c1.measures is p2.measures[0]:
        print("Child measure has reference to parent measure")
    return c1, c2


def uniform(p1, p2):
    c1 = Individual([], None)
    c2 = Individual([], None)
    p1_copy = copy.deepcopy(p1)
    p2_copy = copy.deepcopy(p2)

    for i in range(len(p1_copy.measures)):
        p = rng.choice([True, False])
        if p:
            c1.measures.append(p2_copy.measures[i])
            c2.measures.append(p1_copy.measures[i])
        else:
            c1.measures.append(p1_copy.measures[i])
            c2.measures.append(p2_copy.measures[i])

    if c1.measures[0] is p1.measures[0] or c1.measures[0] is p2.measures[0]:
        print("Child measure has reference to parent measure")

    return c1,c2

