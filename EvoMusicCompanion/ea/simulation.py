from ea import individual, musicPlayer, modelTrainer, initialisation, crossover, mutation, fitness
from ea.individual import Individual


class Simulation:
    pitch_matrix = None
    duration_matrix = None
    learning_rate = 0.5
    population_size = 10
    selection_size = 5

    def __init__(self, learning_rate, population_size, duration_matrix=None, pitch_matrix=None):
        self.learning_rate = learning_rate
        self.population_size = population_size
        self.duration_matrix = duration_matrix
        self.pitch_matrix = pitch_matrix
        self.population: [Individual] = []
        self.elitist_population: [Individual] = []

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

            selected_population = self.population[0:40]
            children = []
            for j in range(1, len(selected_population), 2):
                p1 = selected_population[j - 1]
                p2 = selected_population[j]
                c1, c2 = crossover.measure_crossover(p1, p2)
                mutation.applyMutation(c1)
                mutation.applyMutation(c2)
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
            self.population.extend(children)
            self.population.extend(
                initialisation.initialize_population(60, self.pitch_matrix, self.duration_matrix, None))

            print(f"Iteration {i} done")

        print('Done evolving, playing songs')
        for j in self.population[0:4]:
            print(j)
        musicPlayer.play_music_xml(self.population[0:4])

    def run_interactively(self, pitch_matrix=None, duration_matrix=None, init_vector=None):
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

    def run_with_template(self, pitch_matrix, template):
        self.population = initialisation.initialize_population_by_template(self.population_size, template, 'contour',
                                                                           pitch_matrix)
        return self.population

    def update(self, selection: [individual.Individual] = None):
        if selection is None:
            self.update_matrices(self.population)
        else:
            self.update_matrices(selection)
        self.population = initialisation.initialize_population(self.population_size,
                                                               self.pitch_matrix,
                                                               self.duration_matrix, None)

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
