from ea.individual import Individual, Note, Measure
from music21 import pitch, interval
import random
from ea import fitness, duration, individual, constants
import time
import threading

pitch_matrix = None
duration_matrix = None
backoff_matrix = None

rng = random.Random()

def initialize_population(population_size) -> [Individual]:
    population = []
    for i in range(population_size):
        measures: [Measure] = []
        for j in range(constants.NUM_OF_MEASURES):
            if len(measures) > 0:
                measure_durations = get_duration_for_measure(measures[-1])
            else:
                measure_durations = get_duration_for_measure(None)
            prev_measure = None
            # If there was a previous measure, we take the transitions from last note of that measure
            if len(measures) > 0:
                prev_measure = measures[-1]
            if constants.N_GRAM == 'bigram':
                measure_notes = get_notes_by_duration(measure_durations, prev_measure)
            else:
                measure_notes = get_notes_by_duration_trigram(measure_durations, prev_measure)
            m = Measure(measure_notes, 0, None)
            measures.append(m)
        new_individual = individual.Individual(measures=measures, fitness=0)

        population.append(new_individual)
    # Assign chords to each individual and set fitness
    population = set_chords_for_population(population)
    fitness.set_fitness_for_population(population)
    return population


def init_first_note(init_vector):
    return random_sample(init_vector)


def random_sample(transitions):
    r = rng.random()
    p_sum = 0.0
    for k, v in transitions.iteritems():
        if p_sum < r < p_sum + v:
            return k
        else:
            p_sum += v
    print(f'P_sum = {p_sum}')

    return None


def get_random_pitch_transition(start):
    return get_random_transition(pitch_matrix, start, backoff_matrix)


def get_random_transition(matrix, start, backoff_matrix=None):
    if start is None:
        start = rng.choice(list(matrix.keys()))

    # Backoff case
    if start not in matrix.keys():
        transitions = backoff_matrix[start[1]]
    else:
        transitions = matrix[start]

    sample = random_sample(transitions)

    if sample is None:
        print(f'Cumulative P of {start} does not add up to 1.0')

    return sample


def get_duration_for_measure(prev_measure: individual.Measure):
    dur_counter = 0.0
    durations = []
    while dur_counter < 1.0:
        # 1. Get initial duration
        if dur_counter == 0.0:
            if prev_measure is None:
                new_d = get_random_transition(duration_matrix, None)
            else:
                new_d = get_random_transition(duration_matrix, prev_measure.notes[-1].duration.duration_name)
            new_d = duration.Duration(new_d, None)
            dur_counter += new_d.duration_value
            durations.append(new_d)
            continue

        # 2. Keep generating duration until we reach maximum duration
        new_d = get_random_transition(duration_matrix, durations[-1].duration_name)
        new_d = duration.Duration(new_d, None)

        # 3. If adding next one exceeds: Either lengthen the last note or add a rest
        (exceeds, remaining) = exceeds_duration(new_d.duration_value, dur_counter)

        if exceeds and remaining > 0:
            break
        dur_counter += new_d.duration_value
        durations.append(new_d)

    return durations


def get_notes_by_duration(durations, prev_measure: Measure = None):
    notes = []
    for i in range(len(durations)):
        curr_dur = durations[i]
        if i == 0:
            prev_pitch = None
            if prev_measure is not None:
                prev_pitch = prev_measure.notes[-1].pitch
            curr_pitch = get_random_transition(pitch_matrix, prev_pitch)
            n = Note(curr_pitch, curr_dur)
            notes.append(n)
            continue
        curr_pitch = get_random_transition(pitch_matrix, notes[-1].pitch)
        n = Note(curr_pitch, curr_dur)
        notes.append(n)
    return notes


def get_notes_by_duration_trigram(durations, prev_measure):
    notes = []
    for i in range(len(durations)):
        curr_dur = durations[i]
        if i == 0:
            if prev_measure is not None:
                p1 = prev_measure.notes[len(prev_measure.notes) - 2].pitch
                p2 = prev_measure.notes[-1].pitch
                curr_pitch = get_random_transition(pitch_matrix, (p1, p2), backoff_matrix)
            else:
                curr_pitch = get_random_transition(pitch_matrix, None)
        elif i == 1:
            if prev_measure is not None:
                p1 = prev_measure.notes[-1].pitch
                p2 = notes[-1].pitch
                curr_pitch = get_random_transition(pitch_matrix, (p1, p2), backoff_matrix)
            else:
                curr_pitch = get_random_transition(pitch_matrix, None)
        else:
            p1 = notes[len(notes) - 2].pitch
            p2 = notes[-1].pitch
            curr_pitch = get_random_transition(pitch_matrix, (p1, p2), backoff_matrix)
        n = Note(curr_pitch, curr_dur)
        notes.append(n)
    return notes


def exceeds_duration(new_duration, curr_duration):
    # Check how much duration exceeds when adding the new duration
    total_duration = curr_duration + new_duration

    max_duration_left = 1.0 - curr_duration
    # If this is more than 1.0, we can decrease the length of this duration or we have to remove it
    if total_duration > 1.0:
        # If there is still room for another note, change it to that duration
        if max_duration_left > 0.0:
            return True, max_duration_left
        # Else we do not want to add this note
        else:
            return True, 0.0
    return False, 0.0


def set_chords_for_population(population: [Individual]):
    for i in population:
        set_chords(i)
    return population


def set_chords(individual: Individual):
    chords = [['C3', 'E3', 'G3', 'B3'], ['F3', 'A3', 'C4', 'E4'], ['G3', 'B3', 'D4', 'F4'], ['C3', 'E3', 'G3', 'B3']]
    counter = 0
    for j in range(len(individual.measures)):
        individual.measures[j].set_chord(chords[counter])
        if counter == len(chords) - 1:
            counter = 0
        else:
            counter += 1
