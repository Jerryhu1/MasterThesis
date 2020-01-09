from ea.individual import Individual, Note, Measure
from music21 import pitch, interval
import random
from ea import fitness, duration, individual, constants
import music21


def initialize_population(population_size, pitch_matrix, duration_matrix) -> [Individual]:
    population = []

    for i in range(population_size):
        measures: [Measure] = []
        for j in range(constants.NUM_OF_MEASURES):
            if len(measures) > 0:
                measure_durations = get_duration_for_measure(duration_matrix, measures[-1])
            else:
                measure_durations = get_duration_for_measure(duration_matrix, None)
            prev_measure = None
            # If there was a previous measure, we take the transitions from last note of that measure
            if len(measures) > 0:
                prev_measure = measures[-1]
            if constants.N_GRAM == 'bigram':
                measure_notes = get_notes_by_duration(measure_durations, pitch_matrix, prev_measure)
            else:
                measure_notes = get_notes_by_duration_trigram(measure_durations, pitch_matrix, prev_measure)
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
    rng = random.random()

    p_sum = 0.0
    for k, v in transitions.iteritems():
        if p_sum < rng < p_sum + v:
            return k
        else:
            p_sum += v

    return None


def get_random_transition(matrix, start):
    if start is None:
        start = random.choice(list(matrix.keys()))

    transitions = matrix[start]

    sample = random_sample(transitions)

    if sample is None:
        print(f'Cumulative P of {start} does not add up to 1.0')

    return sample


def initialize_population_interval(population_size, interval_matrix, duration_matrix, init_vector):
    population = []

    for i in range(population_size):
        curr_indiv_notes: [[Note]] = []
        init_note = None

        for j in range(constants.NUM_OF_MEASURES):
            measure: individual.Measure = None
            # Should change this to while duration < measurelength
            while len(measure) < 32:
                is_initial_note = len(measure) == 0 or (len(measure) == 1 and constants.N_GRAM == 'trigram')
                if is_initial_note:
                    next_duration_type = get_random_transition(duration_matrix, None)
                    next_pitch = init_first_note(init_vector)
                    init_note = pitch.Pitch(next_pitch)
                    next_interval = 'P1'
                else:
                    if constants.N_GRAM == 'trigram':
                        prev_durations = (measure[-1].duration.duration_name, measure[-2].duration.duration_name)
                        prev_notes = (measure[-2].pitch, measure[-1].pitch)
                    else:
                        prev_durations = measure[-1].duration.duration_name
                        prev_notes = measure[-1]

                    next_duration_type = get_random_transition(duration_matrix, prev_durations)
                    next_interval = get_random_transition(interval_matrix, prev_notes.interval)

                next_duration = duration.Duration(next_duration_type, None)

                (exceeds, d) = exceeds_duration(measure, next_duration)
                # If the maximum duration is exceeded by the next note, either shorten it or stop
                # if exceeds and d >= 0.015625:
                #     print(f"Exceeded max duration, decreasing it to {d}")
                #     next_duration = duration.Duration(None, d)
                if exceeds:
                    break

                intvl = interval.Interval(next_interval)
                next_pitch = intvl.transposePitch(init_note).nameWithOctave
                next_note = individual.Note(next_pitch, next_duration, intvl.name, init_note)
                measure.append(next_note)

            curr_indiv_notes.append(measure)

        # Create individual and set fitness
        new_individual = individual.Individual(notes=curr_indiv_notes, fitness=0)
        f = fitness.get_fitness(new_individual)
        new_individual.fitness = f

        population.append(new_individual)

    return population


def get_duration_for_measure(duration_matrix, prev_measure: individual.Measure):
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

        # Append to durations
        durations.append(new_d)

    return durations


def get_notes_by_duration(durations, pitch_matrix, prev_measure: Measure = None):
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


def get_notes_by_duration_trigram(durations, pitch_matrix, prev_measure):
    notes = []
    for i in range(len(durations)):
        curr_dur = durations[i]
        if i == 0:
            if prev_measure is not None:
                p1 = prev_measure.notes[len(prev_measure.notes)-2].pitch
                p2 = prev_measure.notes[-1].pitch
                curr_pitch = get_random_transition(pitch_matrix, (p1, p2))
            else:
                curr_pitch = get_random_transition(pitch_matrix, None)
            n = Note(curr_pitch, curr_dur)
            notes.append(n)
        elif i == 1:
            if prev_measure is not None:
                p1 = prev_measure.notes[-1]
                p2 = notes[-1]
                curr_pitch = get_random_transition(pitch_matrix, (p1, p2))
            else:
                curr_pitch = get_random_transition(pitch_matrix, None)
            n = Note(curr_pitch, curr_dur)
            notes.append(n)
        else:
            p1 = notes[len(notes)-2].pitch
            p2 = notes[-1].pitch
            curr_pitch = get_random_transition(pitch_matrix, (p1, p2))
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
        if counter == len(chords):
            counter = 0
        individual.measures[j].set_chord(chords[counter])
        counter += 1

