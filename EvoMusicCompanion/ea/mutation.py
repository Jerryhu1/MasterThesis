from random import Random

from music21 import pitch
from music21.interval import Interval

from ea import initialisation, simulation
from ea.individual import Individual, Measure
import copy

rng = Random()


def applyMutation(individual: Individual, elitist_population: [Individual]):
    mutations = [swap_measure, reverse_measure, elitist_population]

    p1 = 0.2
    p2 = 0.2
    p3 = 0.3

    p = rng.random()

    if p < p1:
        swap_measure(individual)
    if p < p2:
        reverse_measure(individual)
    if p < p3:
        elitist_mutation(individual, elitist_population)


def elitist_mutation(individual: Individual, elitist_population: [Individual]):
    e_individual: Individual = rng.choice(elitist_population)
    measure = rng.choice(e_individual.measures)

    m_measure = rng.randrange(len(individual.measures))
    individual.measures[m_measure].notes = copy.deepcopy(measure.notes)


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
    individual.measures[m_index].notes[n_index2] = n1


def change_rest_or_note(individual: Individual):
    m_index = rng.randrange(len(individual.measures))
    notes = individual.measures[m_index].notes
    note_index = rng.randrange(len(notes))
    note = notes[note_index]
    if note_index > 0:
        prev_note = notes[note_index - 1]
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


def transpose_interval_measure(individual: Individual):
    m: Measure = rng.choice(individual.measures)
    first_pitch = None
    new_first_pitch = None
    for n in m.notes:
        if n.pitch == 'REST':
            continue
        # If we find the first pitch, we tranpose this first
        if first_pitch is None:
            first_pitch = n.pitch
            intvl = Interval(rng.choice([2, 4, 5]))
            curr_octave = n.pitch[1]
            new_first_pitch = intvl.transposePitch(pitch.Pitch(f'C{curr_octave}'), reverse=rng.choice([True, False]))
            n.pitch = new_first_pitch.nameWithOctave
            continue
        # The remaining notes will be transposed with the same intervals as previously
        curr_pitch = pitch.Pitch(n.pitch)
        intvl_first_pitch = Interval(pitch.Pitch(first_pitch), curr_pitch)
        # Transpose the new first pitch to the previous interval
        new_pitch = intvl_first_pitch.transposePitch(new_first_pitch)
        n.pitch = new_pitch.nameWithOctave


def reverse_measure(individual: Individual):
    m: Measure = rng.choice(individual.measures)
    m_copy = copy.deepcopy(m)
    j = len(m.notes) - 1
    for i in range(len(m.notes)):
        m.notes[i] = m_copy.notes[j]
        j -= 1

