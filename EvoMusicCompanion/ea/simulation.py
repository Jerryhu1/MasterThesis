from math import ceil

from ea import individual, musicPlayer, modelTrainer, initialisation, crossover, mutation, fitness, selection, constants, metrics
from ea.individual import Individual
import random


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
            print('Training the pitch matrix, this might take a while')
            self.pitch_matrix = modelTrainer.train_pitch_matrix(None)

        if duration_matrix is None:
            print('Training the duration matrix, this might take a while')
            self.duration_matrix = modelTrainer.train_duration_matrix(None)

        if backoff_matrix is None:
            self.backoff_matrix = modelTrainer.get_backoff_matrix()
        initialisation.pitch_matrix = self.pitch_matrix
        initialisation.duration_matrix= self.duration_matrix
        initialisation.backoff_matrix = self.backoff_matrix

        print('Initializing population')

        print('Starting evolution')
        self.population = initialisation.initialize_population(constants.POPULATION_SIZE)
        for i in range(constants.ITERATIONS):

            #selected_population = selection.tournament_selection(self.population, self.tournament_size)
            #sorted_selection = sorted(selected_population, key=lambda x: x.fitness, reverse=True)

            self.population.sort(key=lambda x: x.fitness, reverse=True)
            self.elitist_population = self.population[0:constants.ELITISM_SIZE]

            next_generation = []
            #next_generation.extend(self.elitist_population)
            random.shuffle(self.population)

            for j in range(0, len(self.population), 2):
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

            next_generation.sort(key=lambda x: x.fitness, reverse=True)
            next_generation = next_generation[0:constants.POPULATION_SIZE]

        # self.update_matrices(selected_population[0:5])
            # New generation:
            # Selected population
            # Children of selection
            # Newly sampled individuals
            self.population = next_generation
            #self.population.extend(
            #    initialisation.initialize_population(self.population_size - len(self.population), self.pitch_matrix,
            #                                         self.duration_matrix, self.backoff_matrix))

            fitnesses = list(map(lambda x: x.fitness, self.population))
            avg_fitness = sum(fitnesses) / len(self.population)
            metrics.write_population_metrics(i, self.population)
            print(f"Iteration {i} done")
            print(f"Max chord beat fitness {self.population[0].fitnesses['C_TONE_B']}")
            # print(f"Average fitness: {avg_fitness}")
            # print(f"Max fitness: {max(fitnesses)}")
            # print(f"Min fitness: {min(fitnesses)}")
            # print(f"Population size: {len(self.population)}")
            # print(f"Proportion of equal individuals: {metrics.proportion_equal_to_highest_fitness(self.population)}")
        print('-------------------------------------------------')
        print('Done evolving, playing songs')
        # for j in range(len(self.population[0:4])):
        #     ind = self.population[j]
        #     print(f'Individual: {j}')
        #     fitness.print_fitness_values(ind)
        #     print(f' ')

        print(f'Population size: {constants.POPULATION_SIZE}')
        print(f'Elitist population size: {len(self.elitist_population)}')
        print(f'Tournament size: {constants.TOURNAMENT_SIZE}')
        print(f'Iterations: {constants.ITERATIONS}')
        print(f'Model updating: None, ratio = N/A')
        play_pieces = [self.population[0], self.population[ceil(len(self.population)/2)], self.population[-1]]
        # for j in range(len(play_pieces)):
        #     ind = play_pieces[j]
        #     print(f'Individual: {j}')
        #     fitness.print_fitness_values(ind)
        #     print(f' ')
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        musicPlayer.write_music_midi(play_pieces)

    def run_interactively(self, pitch_matrix=None, duration_matrix=None):
        print('Starting generation')

        if pitch_matrix is None:
            print('Training the pitch matrix, this might take a while')
            self.pitch_matrix = modelTrainer.train_pitch_matrix(None)
        else:
            self.pitch_matrix = pitch_matrix

        if duration_matrix is None:
            print('Training the duration matrix, this might take a while')
            self.duration_matrix = modelTrainer.train_duration_matrix(None)
        else:
            self.duration_matrix = duration_matrix
        self.population = initialisation.initialize_population(self.population_size,
                                                               self.pitch_matrix, self.duration_matrix)
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        return self.population

    def update(self, selection: [individual.Individual] = None):
        if selection is None:
            self.update_matrices(self.population)
        else:
            self.update_matrices(selection)
        self.population = initialisation.initialize_population(self.population_size,
                                                               self.pitch_matrix,
                                                               self.duration_matrix)

        self.population.sort(key=lambda x: x.fitness, reverse=True)

        return self.population[0:self.selection_size]

    def update_matrices(self, selection):
        selected_population_pitches = []
        selected_population_durations = []
        for s in selection:
            pitch_measure = []
            duration_measure = []
            for m in s.measures:
                for n in m.notes:
                    pitch_measure.append(n.pitch)
                    duration_measure.append(n.duration.duration_name)
            selected_population_pitches.append(pitch_measure)
            selected_population_durations.append(duration_measure)

        self.pitch_matrix = modelTrainer.update_matrix(selected_population_pitches, self.pitch_matrix, 0.8)
        # self.duration_matrix = modelTrainer.update_matrix(selected_population_durations, self.duration_matrix, 0.8)

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