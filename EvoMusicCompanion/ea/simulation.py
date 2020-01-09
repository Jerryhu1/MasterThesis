from ea import individual, musicPlayer, modelTrainer, initialisation, crossover, mutation, fitness, selection
from ea.individual import Individual


class Simulation:
    pitch_matrix = None
    duration_matrix = None
    learning_rate = 0.5
    population_size = 10
    selection_size = 5
    simulation = None
    tournament_size = 4
    elitism_size = 5

    def __init__(self, learning_rate, population_size, duration_matrix=None, pitch_matrix=None):
        if self.simulation is not None:
            print('Two instances of simulation, killing one')
        self.learning_rate = learning_rate
        self.population_size = population_size
        self.duration_matrix = duration_matrix
        self.pitch_matrix = pitch_matrix
        self.population: [Individual] = []
        self.elitist_population: [Individual] = []
        self.simulation = self

    def run(self, iterations, pitch_matrix, duration_matrix):
        print('Starting generation')

        if pitch_matrix is None:
            print('Training the pitch matrix, this might take a while')
            self.pitch_matrix = modelTrainer.train_pitch_matrix(None)

        if duration_matrix is None:
            print('Training the duration matrix, this might take a while')
            self.duration_matrix = modelTrainer.train_duration_matrix(None)

        print('Initializing population')

        print('Starting evolution')
        self.population = initialisation.initialize_population(self.population_size, self.pitch_matrix,
                                                               self.duration_matrix)
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

            avg_fitness = sum(map(lambda x: x.fitness, self.population)) / len(self.population)
            print(f"Average fitness: {avg_fitness}")

            # self.update_matrices(selected_population[0:5])
            # New generation:
            # Selected population
            # Children of selection
            # Newly sampled individuals
            self.population = []
            self.population.extend(self.elitist_population)
            self.population.extend(children)
            self.population.extend(
                initialisation.initialize_population(self.population_size - len(self.population), self.pitch_matrix, self.duration_matrix))

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

        musicPlayer.play_music_xml([self.population[0]])

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
