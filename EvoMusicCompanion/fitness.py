major_scale = ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5']


def get_fitness(individual):
    counter = 0
    for note in individual:
        if note in major_scale:
            counter += 1

    return counter / len(individual)
