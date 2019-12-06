from ea.individual import Individual, Note, Measure
from music21 import pitch, interval
import random
from ea import fitness, duration, individual, constants
import music21


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


def initialize_population(population_size, pitch_matrix, duration_matrix, init_vector) -> [Individual]:
    population = []

    for i in range(population_size):
        curr_indiv_measures: [Measure] = []
        for j in range(constants.NUM_OF_MEASURES):
            notes_in_measure: [Note] = []
            # Should change this to while duration < measurelength
            while len(notes_in_measure) < 32:
                is_initial_note = len(notes_in_measure) == 0 or (len(notes_in_measure) == 1 and constants.N_GRAM == 'trigram')
                if is_initial_note:
                    next_duration_type = get_random_transition(duration_matrix, None)
                    if init_vector is None:
                        next_pitch = get_random_transition(pitch_matrix, None)
                        next_duration_type = get_random_transition(duration_matrix, None)
                    else:
                        next_pitch = init_first_note(init_vector)
                else:
                    if constants.N_GRAM == 'trigram':
                        prev_durations = (notes_in_measure[-1].duration.duration_name, notes_in_measure[-2].duration.duration_name)
                        prev_notes = (notes_in_measure[-2].pitch, notes_in_measure[-1].pitch)
                    else:
                        prev_durations = notes_in_measure[-1].duration.duration_name
                        prev_notes = notes_in_measure[-1].pitch

                    next_duration_type = get_random_transition(duration_matrix, prev_durations)
                    next_pitch = get_random_transition(pitch_matrix, prev_notes)

                next_duration = duration.Duration(next_duration_type, None)

                (exceeds, d) = exceeds_duration(notes_in_measure, next_duration)
                # If the maximum duration is exceeded by the next note, either shorten it or stop
                # if exceeds and d >= 0.015625:
                #     print(f"Exceeded max duration, decreasing it to {d}")
                #     next_duration = duration.Duration(None, d)
                if exceeds:
                    break
                next_note = individual.Note(next_pitch, next_duration)
                notes_in_measure.append(next_note)

            new_measure = Measure(notes_in_measure, 0, None)
            curr_indiv_measures.append(new_measure)

        # Create individual
        new_individual = individual.Individual(measures=curr_indiv_measures, fitness=0)

        population.append(new_individual)

    # Assign chords to each individual and set fitness
    population = set_chords(population)
    fitness.set_fitness(population)

    return population


def set_chords(population: [Individual]):
    chords = [['C3', 'E3', 'G3'], ['F3', 'A3', 'C3'], ['G3', 'B3', 'D3']]
    counter = 0
    for i in population:
        for j in i.measures:
            j.set_chord(chords[counter])
            counter += 1
            if counter == 3:
                counter = 0
    return population


def exceeds_duration(notes, new_duration) -> (bool, float):
    # Check how much duration exceeds when adding the new duration
    prev_total_duration = sum([i.duration_value for i in [j.duration for j in notes]])
    total_duration = prev_total_duration + new_duration.duration_value

    max_duration_left = 1.0 - prev_total_duration
    # If this is more than 1.0, we can decrease the length of this duration or we have to remove it
    if total_duration > 1.0:
        # If there is still room for another note, change it to that duration
        if max_duration_left > 0.0:
            return True, max_duration_left
        # Else we do not want to add this note
        else:
            return True, 0.0

    return False, 0.0


def initialize_population_by_template(population_size, template, mode, matrix):
    population = []
    for i in range(population_size):
        if mode == 'contour':
            notes = []
            for c in template:
                if len(notes) == 0:
                    next_pitch = get_pitch_transition_by_contour('C4', c, matrix)
                else:
                    next_pitch = get_pitch_transition_by_contour(notes[-1], c, matrix)
                    if next_pitch is None:
                        # Do something when we are in unsatisfiable state.
                        next_pitch = 'C4'

                notes.append(next_pitch)
        population.append(notes)
    return population


def get_pitch_transition_by_contour(pitch, contour, matrix):
    transitions = matrix[pitch]

    t_contour = {}

    for k, v in transitions.iteritems():
        if k == ' ':
            continue
        if contour == 'h':
            if music21.note.Note(k) > music21.note.Note(pitch):
                t_contour[k] = v
        elif contour == 'l':
            if music21.note.Note(k) < music21.note.Note(pitch):
                t_contour[k] = v
        elif contour == 'b':
            if music21.note.Note(k) >= music21.note.Note(pitch):
                t_contour[k] = v
        elif contour == 'p':
            if music21.note.Note(k) <= music21.note.Note(pitch):
                t_contour[k] = v
        elif contour == 'e':
            if music21.note.Note(k) == music21.note.Note(pitch):
                t_contour[k] = v
        else:
            t_contour[k] = v

    rng = random.random()
    p_sum = 0.0
    # Normalize probability
    p_total = sum(t_contour.values())

    for k in t_contour:
        norm_p = t_contour[k] / p_total
        t_contour[k] = norm_p

        if p_sum < rng < p_sum + norm_p:
            return k
        else:
            p_sum += t_contour[k]

    print(f'rng: {rng}')
    print(f'p_sum: {p_sum}')
    print('P does not sum to 1.0')
