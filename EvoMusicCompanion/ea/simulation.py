from math import ceil

from ea import individual, musicPlayer, modelTrainer, initialisation, crossover, mutation, fitness, selection, \
    constants, metrics, modelUpdater
from ea.individual import Individual
import random
import time
import sys


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
        print('Starting generation')
        if pitch_matrix is None:
            self.pitch_matrix = modelTrainer.train_pitch_matrix(None)

        if duration_matrix is None:
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
            self.population.sort(key=lambda x: x.fitness)
            self.elitist_population = self.population[0:constants.ELITISM_SIZE]

            next_generation = []

            if constants.SYSTEM == "GA" or constants.SYSTEM == "HYBRID":
                random.shuffle(self.population)
                if constants.CROSSOVER == "NONE":
                    self.mutation_only()
                    next_generation.extend(self.population)
                else:
                    crossover_generation = self.crossover_mutation()
                    crossover_generation.sort(key=lambda x: x.fitness)
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

            next_generation.sort(key=lambda x: x.fitness)
            next_generation = next_generation[0:constants.POPULATION_SIZE]

            self.population = next_generation

            # Metrics

            if constants.SYSTEM is not "MULTIPLE" and constants.METRIC_MODE is not "ALL":
                metrics.write_population_metrics(i, self.population)

            if constants.METRIC_MODE == "ALL":
                metrics.write_individual_metrics(i, population=self.population)

            if i % 25 == 0:
                print(f"Iteration {i} done")
                print(f'Highest fitness: {self.population[0].fitness}')


            sys.stdout.flush()
        self.population.sort(key=lambda x: x.fitness)


        if constants.RUN_MODE == 'MULTIPLE':
            metrics.write_average_runs(converged_iteration, self.population)
        if constants.SYSTEM != 'GA':
            metrics.write_matrices(self.pitch_matrix, self.backoff_matrix, self.duration_matrix)

        play_pieces = [self.population[0], self.population[ceil(len(self.population) / 2)], self.population[-1]]
        musicPlayer.write_music_midi(play_pieces)

        if constants.RUN_MODE == "SINGLE":
            print('-------------------------------------------------')
            print('Done evolving, playing songs')
            print(f'Population size: {constants.POPULATION_SIZE}')
            print(f'Elitist population size: {len(self.elitist_population)}')
            print(f'Tournament size: {constants.TOURNAMENT_SIZE}')
            print(f'Iterations: {constants.ITERATIONS}')
            print(f'Model updating: None, ratio = N/A')

        sys.stdout.flush()

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
            family.sort(key=lambda x: x.fitness)
            next_generation.extend(family[0:2])
        return next_generation
