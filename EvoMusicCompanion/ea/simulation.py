from math import ceil

from ea import individual, musicPlayer, modelTrainer, initialisation, crossover, mutation, fitness, selection, \
    constants, metrics, modelUpdater
from ea.individual import Individual
import random
import time

class Simulation:
    pitch_matrix = None
    backoff_matrix = None
    duration_matrix = None
    simulation = None

    def __init__(self, duration_matrix=None, pitch_matrix=None):
        if self.simulation is not None:
            print('Two instances of simulation, killing one')
        self.duration_matrix = duration_matrix
        self.pitch_matrix = pitch_matrix
        self.population: [Individual] = []
        self.elitist_population: [Individual] = []
        self.simulation = self

    def run(self, pitch_matrix, duration_matrix, backoff_matrix):
        start = time.time()
        print('Starting generation')
        if pitch_matrix is None:
            print('Training the pitch matrix, this might take a while')
            self.pitch_matrix = modelTrainer.train_pitch_matrix(None)

        if duration_matrix is None:
            print('Training the duration matrix, this might take a while')
            self.duration_matrix = modelTrainer.train_duration_matrix(None)

        if backoff_matrix is None:
            self.backoff_matrix = modelTrainer.get_backoff_matrix()
        initialisation.pitch_matrix = self.pitch_matrix
        initialisation.duration_matrix = self.duration_matrix
        initialisation.backoff_matrix = self.backoff_matrix

        print('Initializing population')

        self.population = initialisation.initialize_population(constants.POPULATION_SIZE)
        converged_counter = 0.0
        converged_iteration = -1

        for i in range(constants.ITERATIONS):
            self.population.sort(key=lambda x: x.fitness, reverse=True)
            self.elitist_population = self.population[0:constants.ELITISM_SIZE]

            next_generation = []

            if constants.SYSTEM == "GA" or constants.SYSTEM == "HYBRID":
                random.shuffle(self.population)
                if constants.CROSSOVER == "NONE":
                    self.mutation_only()
                    next_generation.extend(self.population)
                else:
                    crossover_generation = self.crossover_mutation()
                    crossover_generation.sort(key=lambda x: x.fitness, reverse=True)
                    if constants.SYSTEM == "HYBRID":
                        next_generation.extend(crossover_generation[0:constants.CROSSOVER_POPULATION])
                    else:
                        next_generation.extend(crossover_generation)


            if constants.SYSTEM == "MODEL" or constants.SYSTEM == "HYBRID":
                # Elitism
                next_generation.extend(self.elitist_population)
                sel = self.population[0:constants.SELECTION_SIZE]
                if constants.LEARNING_RATE != 0.0:
                    self.update_matrices(sel)
            if constants.SYSTEM == "HYBRID":
                next_generation.extend(initialisation.initialize_population(constants.MODEL_POPULATION))
            else:
                next_generation.extend(
                        initialisation.initialize_population(constants.POPULATION_SIZE))



            next_generation.sort(key=lambda x: x.fitness, reverse=True)
            next_generation = next_generation[0:constants.POPULATION_SIZE]

            self.population = next_generation

            # Metrics
            if constants.SYSTEM is not "MULTIPLE" and constants.METRIC_MODE is not "ALL":
                metrics.write_population_metrics(i, self.population)

            if i % 25 == 0:
                print(f"Iteration {i} done")

            if constants.METRIC_MODE == "ALL":
                metrics.write_individual_metrics(i, population=self.population)

            if metrics.converged(self.population):
                converged_counter += 1
            else:
                converged_counter = 0
            if converged_counter > 10:
                print('Population is converged, stopping')
                converged_iteration = i-10
                break

            end = time.time()
            print(f'Iteration time: {end-start}')
            # print(f"Average fitness: {avg_fitness}")
            # print(f"Max fitness: {max(fitnesses)}")
            # print(f"Min fitness: {min(fitnesses)}")
            # print(f"Population size: {len(self.population)}")
            # print(f"Proportion of equal individuals: {metrics.proportion_equal_to_highest_fitness(self.population)}")
        print('-------------------------------------------------')
        print('Done evolving, playing songs')
        print(f'Population size: {constants.POPULATION_SIZE}')
        print(f'Elitist population size: {len(self.elitist_population)}')
        print(f'Tournament size: {constants.TOURNAMENT_SIZE}')
        print(f'Iterations: {constants.ITERATIONS}')
        print(f'Model updating: None, ratio = N/A')
        play_pieces = [self.population[0], self.population[ceil(len(self.population) / 2)], self.population[-1]]
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        if constants.RUN_MODE == 'MULTIPLE':
            metrics.write_average_runs(converged_iteration, self.population)

        if constants.SYSTEM != 'GA':
            metrics.write_matrices(self.pitch_matrix, self.backoff_matrix, self.duration_matrix)
        musicPlayer.write_music_midi(play_pieces)

    def crossover_mutation(self):
        next_generation = []
        random.shuffle(self.population)
        for j in range(1, len(self.population), 2):
            family = []
            p1 = self.population[j - 1]
            p2 = self.population[j]
            c1, c2 = crossover.measure_crossover(p1, p2)
            mutation.applyMutation(c1, self.elitist_population)
            mutation.applyMutation(c2, self.elitist_population)
            fitness.set_fitness(c1)
            fitness.set_fitness(c2)
            family.extend([c1, c2, p1, p2])
            family.sort(key=lambda x: x.fitness, reverse=True)
            next_generation.extend(family[0:2])
        return next_generation

    def mutation_only(self):
        for i in self.population:
            mutation.applyMutation(i, self.elitist_population)
            fitness.set_fitness(i)

    def update_matrices(self, individuals):
        self.pitch_matrix = modelUpdater.update_matrix(individuals, self.pitch_matrix)
        self.backoff_matrix = modelUpdater.update_matrix(individuals, self.backoff_matrix, True)
        self.duration_matrix = modelUpdater.update_duration(individuals, self.duration_matrix)
        initialisation.backoff_matrix = self.backoff_matrix
        initialisation.pitch_matrix = self.pitch_matrix


def run_with_corpus(self, corpus: [Individual], iterations, pitch_matrix, duration_matrix, backoff_matrix):
    print('Starting generation')
    if pitch_matrix is None:
        print('Training the pitch matrix, this might take a while')
        self.pitch_matrix = modelTrainer.train_pitch_matrix(None)

    if duration_matrix is None:
        print('Training the duration matrix, this might take a while')
        self.duration_matrix = modelTrainer.train_duration_matrix(None)

    if backoff_matrix is None:
        self.backoff_matrix = modelTrainer.get_backoff_matrix()

    print('Initializing population')

    print('Starting evolution')
    self.population = corpus
    init_pop = initialisation.initialize_population(self.population_size, self.pitch_matrix,
                                                    self.duration_matrix, self.backoff_matrix)
    self.population.extend(init_pop)
    for i in range(iterations):

        self.population.sort(key=lambda x: x.fitness, reverse=True)

        selected_population = selection.tournament_selection(self.population, self.tournament_size)
        sorted_selection = sorted(selected_population, key=lambda x: x.fitness, reverse=True)
        self.elitist_population = sorted_selection[0:self.elitism_size]
        children = []

        for j in range(0, len(selected_population), 2):
            p1 = selected_population[j - 1]
            p2 = selected_population[j]
            c1, c2 = crossover.measure_crossover(p1, p2)
            mutation.applyMutation(c1, self.elitist_population)
            mutation.applyMutation(c2, self.elitist_population)
            fitness.set_fitness(c1)
            fitness.set_fitness(c2)
            children.append(c1)
            children.append(c2)

        fitnesses = list(map(lambda x: x.fitness, self.population))
        avg_fitness = sum(fitnesses) / len(self.population)
        print(f"Average fitness: {avg_fitness}")
        print(f"Max fitness: {max(fitnesses)}")

        # self.update_matrices(selected_population[0:5])
        # New generation:
        # Selected population
        # Children of selection
        # Newly sampled individuals
        self.population = []
        self.population.extend(self.elitist_population)
        self.population.extend(children)
        self.population.extend(
            initialisation.initialize_population(self.population_size - len(self.population), self.pitch_matrix,
                                                 self.duration_matrix, self.backoff_matrix))
        print(f"Iteration {i} done")
    print('-------------------------------------------------')
    print('Done evolving, playing songs')
    for j in range(len(self.population[0:4])):
        ind = self.population[j]
        print(f'Individual: {j}')
        fitness.print_fitness_values(ind)
        print(f' ')

    print(f'Population size: {self.population_size}')
    print(f'Elitist population size: {len(self.elitist_population)}')
    print(f'Tournament size: {self.tournament_size}')
    print(f'Model updating: None, ratio = N/A')

    musicPlayer.play_music_xml(self.population[0:4])
