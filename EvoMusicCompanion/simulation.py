import modelTrainer
import musicPlayer
import initialisation
import individual
import constants


class Simulation:
    pitch_matrix = None
    duration_matrix = None
    learning_rate = 0.5
    population_size = 10

    def __init__(self, learning_rate, population_size):
        self.learning_rate = learning_rate
        self.population_size = population_size

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
        for i in range(iterations):
            population = initialisation.initialize_population(self.population_size, self.pitch_matrix,
                                                              self.duration_matrix, None)
            population.sort(key=lambda x: x.fitness, reverse=True)
            selected_population = population[0:3]
            self.update_matrices(selected_population)

            avg_fitness = sum(map(lambda x: x.fitness, selected_population)) / len(selected_population)
            print(f"Iteration {i} done")
            print(f"Average fitness: {avg_fitness}")

        print('Done evolving, playing songs')
        for j in population[0:4]:
            print(j)
        musicPlayer.play(population)

    def run_interactively(self, pitch_matrix, duration_matrix, init_vector):
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

        population = initialisation.initialize_population(self.population_size,
                                                          self.pitch_matrix, self.duration_matrix, init_vector)
        population.sort(key=lambda x: x.fitness, reverse=True)

        return population

    def run_with_template(self, pitch_matrix, template):
        population = initialisation.initialize_population_by_template(self.population_size, template, 'contour', pitch_matrix)
        return population

    def update_with_measures(self, selection: [individual.Measure]):
        [y.pitch for y in selection.notes]
        map(lambda m: m.notes, selection)

    def update(self, selection: [individual.Individual]):
        self.update_matrices(selection)
        population = initialisation.initialize_population(self.population_size, self.
                                                          pitch_matrix, self.duration_matrix, None)

        return population

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

        # TODO: Update duration matrix
        self.pitch_matrix = modelTrainer.update_matrix(selected_population_pitches, self.pitch_matrix, 0.8)
        #self.duration_matrix = modelTrainer.update_matrix(selected_population_durations, self.duration_matrix, 0.8)
