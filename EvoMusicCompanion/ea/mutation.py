from random import Random

from ea import initialisation, simulation
from ea.individual import Individual, Measure, Note

rng = Random()


def applyMutation(individual: Individual):
    if rng.random() > 0.1:
        swap_measure(individual)


def swap_measure(individual: Individual):
    i1 = rng.randrange(len(individual.measures))
    i2 = rng.randrange(len(individual.measures))
    while i1 == i2:
        i2 = rng.randrange(len(individual.measures) - 1)
    m1 = individual.measures[i1]
    m2 = individual.measures[i2]
    individual.measures[i1] = m2
    individual.measures[i2] = m1


def swap_notes_in_measure(individual: Individual):
    m_index = rng.randrange(len(individual.measures))
    notes = individual.measures[m_index].notes
    n_index1 = rng.randrange(len(notes))
    n_index2 = rng.randrange(len(notes))
    while n_index1 == n_index2:
        n_index2 = rng.randrange(len(notes))
    n1 = notes[n_index1]
    n2 = notes[n_index2]
    individual.measures[m_index].notes[n_index1] = n2
    individual.measures[m_index].notes[n_index2] = n2


def change_rest_or_note(individual: Individual):
    m_index = rng.randrange(len(individual.measures))
    notes = individual.measures[m_index].notes
    note_index = rng.randrange(len(notes))
    note = notes[note_index]
    if note_index > 0:
        prev_note = notes[note_index-1]
    else:
        prev_note = None

    if note.pitch == 'REST':
        note.pitch = initialisation.get_random_transition(simulation.Simulation.pitch_matrix, prev_note)
    else:
        note.pitch = 'REST'
    notes[note_index] = note


def mutate_note_pitch(size: int, individual: Individual):
    for i in range(size):
        m = rng.choice(individual.measures)
        note = rng.choice(m.notes)

