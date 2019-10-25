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
            population = initialisation.initialize_population(self.population_size, 8, self.pitch_matrix,
                                                              self.duration_matrix)
            population.sort(key=lambda x: x[1], reverse=True)
            selected_population = population[0:3]
            selected_population_notes = list(map(lambda x: x[0], selected_population))
            selected_population_pitches = list(map(lambda x: list(map(lambda y: y[0], x)), selected_population_notes))
            self.pitch_matrix = modelTrainer.update_pitch_matrix(selected_population_pitches, self.pitch_matrix, 0.8)

            avg_fitness = sum(map(lambda x: x[1], selected_population)) / len(selected_population)
            print(f"Iteration {i} done")
            print(f"Average fitness: {avg_fitness}")

        print('Done evolving, playing songs')
        for j in population:
            print(j)
        musicPlayer.play(population)

    def run_interactively(self, pitch_matrix, duration_matrix):
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

        population = initialisation.initialize_population(self.population_size, 8, self.pitch_matrix, self.duration_matrix)
        population.sort(key=lambda x: x.fitness, reverse=True)

        return population

    def update(self, selection: [individual.Individual]):
        selected_population_notes = constants.flatten(list(map(lambda x: x.notes, selection)))
        selected_population_pitches = list(map(lambda x: x.pitch, selected_population_notes))
        self.pitch_matrix = modelTrainer.update_pitch_matrix(selected_population_pitches, self.pitch_matrix, 0.8)
        population = initialisation.initialize_population(self.population_size, 8, self.pitch_matrix, self.duration_matrix)

        return population

