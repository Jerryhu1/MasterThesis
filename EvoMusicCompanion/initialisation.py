import random
import fitness
import individual
import duration
import constants


def get_random_transition(matrix, start_note):
    rng = random.random()

    if start_note is None:
        transitions = matrix[' ']
    else:
        transitions = matrix[start_note]

    p_sum = 0.0

    for k, v in transitions.iteritems():
        if p_sum < rng < p_sum + v:
            return k
        else:
            p_sum += v

    print(f'P of {start_note} does not add up to 1.0')
    print(f'Sum = {p_sum}')
    print(f'Rng = {rng}')


def get_random_duration(duration_matrix, start_duration):
    rng = random.random()
    if start_duration is None:
        start_duration = 'eighth'

    transitions = duration_matrix[start_duration]
    p_sum = 0.0

    for k, v in transitions.iteritems():
        if p_sum < rng < p_sum + v:
            return k
        else:
            p_sum += v

    print(f'P of {start_duration} does not add up to 1.0')
    print(f'Sum = {p_sum}')
    print(f'Rng = {rng}')
    return duration_matrix[start_duration]['quarter']


def initialize_population(population_size, measure_length, pitch_matrix, duration_matrix) -> [individual.Individual]:
    population = []

    for i in range(population_size):
        curr_indiv_notes: [[individual.Note]] = []
        for j in range(measure_length):
            measure: [individual.Note] = []
            while len(measure) < 32:

                if len(measure) == 0:
                    next_pitch = get_random_transition(pitch_matrix, None)
                    next_duration_type = get_random_duration(duration_matrix, None)
                else:
                    next_duration_type = get_random_duration(duration_matrix, measure[-1].duration.duration_name)
                    next_pitch = get_random_transition(pitch_matrix, measure[-1].pitch)

                next_duration = duration.Duration(next_duration_type, None)

                (exceeds, d) = exceeds_duration(measure, next_duration)
                # If the maximum duration is exceeded by the next note, either shorten it or stop
                if exceeds and d >= 0.015625:
                    print(f"Exceeded max duration decreasing it to {d}")
                    next_duration = duration.Duration(None, d)
                elif exceeds:
                    break
                next_note = individual.Note(next_pitch, next_duration)
                measure.append(next_note)

            curr_indiv_notes.append(measure)

        # Create individual and set fitness
        new_individual = individual.Individual(curr_indiv_notes, 0)
        f = fitness.get_fitness(new_individual)
        new_individual.fitness = f

        population.append(new_individual)

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
