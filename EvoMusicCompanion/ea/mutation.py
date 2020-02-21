from random import Random

from music21 import pitch
from music21.interval import Interval

from ea import initialisation, simulation, constants, duration
from ea.individual import Individual, Measure
import copy

rng = Random()


def applyMutation(individual: Individual, elitist_population: [Individual]):
    mutations = [swap_measure, change_rest_or_note, change_duration, reverse_measure,
                 transpose_interval_measure, elitist_mutation]
    p1 = 0.2
    p2 = 0.2
    p3 = 0.1
    p4 = 0.1
    p5 = 0.2
    p6 = 0.05
    probs = [p1, p2, p3, p4, p5, p6]

    for i in range(len(mutations)):
        prob = probs[i]
        m = mutations[i]
        p = rng.random()
        if p < prob:
            if m is elitist_mutation:
                m(individual, elitist_population)
            else:
                m(individual)


def elitist_mutation(individual: Individual, elitist_population: [Individual]):
    e_individual: Individual = rng.choice(elitist_population)

    measure = rng.choice(range(len(e_individual.measures)))
    e_individual_copy = copy.deepcopy(e_individual.measures[measure].notes)

    individual.measures[measure].notes = e_individual_copy

    if individual.measures[measure].notes is e_individual.measures[measure].notes:
        print('Mutated individual has reference to elitist individual')


def swap_measure(individual: Individual):
    i1 = rng.randrange(len(individual.measures))
    i2 = rng.randrange(len(individual.measures))
    while i1 == i2:
        i2 = rng.randrange(len(individual.measures) - 1)
    m1 = copy.deepcopy(individual.measures[i1].notes)
    m2 = copy.deepcopy(individual.measures[i2].notes)
    individual.measures[i1].notes = m2
    individual.measures[i2].notes = m1


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
    if note.pitch == 'REST':
        new_pitch = initialisation.get_random_pitch_transition(None)
        note.set_pitch(new_pitch)
    else:
        note.set_pitch('REST')
    notes[note_index] = note


def change_duration(individual: Individual):
    measure = rng.choice(individual.measures)
    notes = measure.notes
    note = rng.choice(notes)
    durations = [0.0625, 0.125, 0.25, 0.5]
    d = rng.choice(durations)
    new_d = duration.Duration(None, d)
    note.duration = new_d
    while measure.get_total_duration() > 1.0:
        n = rng.choice(notes)
        if n is note:
            continue
        n_dur_idx = durations.index(n.duration.duration_value)
        # If this is a sixteenth note, we remove it
        if n_dur_idx == 0:
            measure.notes.pop(n_dur_idx)
        # Else we go one step back in duration
        else:
            new_d = duration.Duration(None, durations[n_dur_idx - 1])
            n.duration = new_d


def change_pitch(size: int, individual: Individual):
    for i in range(size):
        m = rng.choice(individual.measures)
        note = rng.choice(m.notes)


def transpose_interval_measure(individual: Individual):
    m: Measure = rng.choice(individual.measures)
    intvl = 0

    for i in range(len(m.notes)):
        n = m.notes[i]
        if n.pitch == 'REST':
            continue
        # If we find the first pitch, we transpose this first
        if i == 0:
            first_pitch = n.pitch
            intvl = (rng.choice([1, 2, 3]))
            init_scale_degree = constants.NOTE_RANGE.index(first_pitch)

            if len(constants.NOTE_RANGE) - init_scale_degree < 13:
                intvl = -intvl

            # If the new scale degree is not in range, we set it to the minimum or maximum
            if init_scale_degree + intvl < 0:
                new_first_pitch = constants.NOTE_RANGE[0]
            elif init_scale_degree + intvl > len(constants.NOTE_RANGE) - 1:
                new_first_pitch = constants.NOTE_RANGE[-1]
            else:
                new_first_pitch = constants.NOTE_RANGE[init_scale_degree + intvl]

            n.set_pitch(new_first_pitch)
            continue

        note_scale_degree = constants.NOTE_RANGE.index(n.pitch)
        # The remaining notes will be transposed with the same intervals as previously
        # If the note goes out of range, we lower or raise with an octave
        if note_scale_degree + intvl > len(constants.NOTE_RANGE) - 1:
            intvl = intvl - 7
        elif note_scale_degree + intvl < 0:
            intvl = intvl + 7

        new_pitch = constants.NOTE_RANGE[note_scale_degree + intvl]
        n.set_pitch(new_pitch)


def reverse_measure(individual: Individual):
    m: Measure = rng.choice(individual.measures)
    m_copy = copy.deepcopy(m)
    j = len(m.notes) - 1
    for i in range(len(m.notes)):
        m.notes[i] = m_copy.notes[j]
        j -= 1
