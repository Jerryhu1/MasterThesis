import random
import fitness


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


def initialize_population(population_size, measure_length, pitch_matrix, duration_matrix):
    population = []

    for i in range(population_size):
        individual = []
        for j in range(measure_length):

            while len(individual) < measure_length:
                if len(individual) == 0:
                    # Add durations
                    next_pitch = get_random_transition(pitch_matrix, None)
                    next_duration = get_random_duration(duration_matrix, None)
                else:
                    # Add durations
                    next_duration = get_random_duration(duration_matrix, individual[-1][1])
                    next_pitch = get_random_transition(pitch_matrix, individual[-1][0])

                next_note = (next_pitch, next_duration)
                individual.append(next_note)

        f = fitness.get_fitness(individual[0])

        population.append((individual, f))

    return population
