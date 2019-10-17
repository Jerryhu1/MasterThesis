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


def initialize_population(population_size, measure_length, matrix):
    population = []

    for i in range(population_size):
        individual = []
        for j in range(measure_length):

            while len(individual) < measure_length:
                if len(individual) == 0:
                    # Add durations
                    next_note = get_random_transition(matrix, None)
                else:
                    # Add durations
                    next_note = get_random_transition(matrix, individual[-1])
                individual.append(next_note)

        f = fitness.get_fitness(individual)

        population.append((individual, f))

    return population
