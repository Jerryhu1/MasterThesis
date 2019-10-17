import modelTrainer
import musicPlayer
import initialisation
import random

def run(iterations, population_size, matrix):
    print('Starting generation')

    if matrix is None:
        print('Training the matrix, this might take a while')
        model = modelTrainer.train()
    else:
        model = matrix

    print('Initializing population')

    print('Starting evolution')
    for i in range(iterations):
        population = initialisation.initialize_population(population_size, 8, model)
        population.sort(key=lambda x: x[1], reverse=True)
        selected_population = population[0:3]
        selected_population_notes = list(map(lambda x: x[0], selected_population))

        model = modelTrainer.update_matrix(selected_population_notes, model, 0.8)

        avg_fitness = sum(map(lambda x: x[1], selected_population)) / len(selected_population)
        print(f"Iteration {i} done")
        print(f"Average fitness: {avg_fitness}")

    print('Done evolving, playing songs')
    for j in population:
        print(j)
    musicPlayer.play(population)