import collections

from ea import util, constants
from ea.individual import Individual
import csv
import os
import datetime
import pandas as pd

def write_population_metrics(iteration, population: [Individual]):
    header = ["i", "MAX_F", "MIN_F", "MEAN_F", "C_TONE", "C_TONE_B", "CADENCE", "L_NOTE", "I_RES", "L_INT", "L_DUR",
              "CONS_R", "CONS_N", "PATTERN_D", "PATTERN_SD", "EQ_INDIV", "INDIV_SIZE", "L_RATE", "POP_SIZE", "E_SIZE", "X_TYPE"]
    fitnesses = list(map(lambda x: x.fitness, population))
    avg_fitness = sum(fitnesses) / len(population)
    max_fitness = max(fitnesses)
    min_fitness = min(fitnesses)

    c_tone = population[0].fitnesses['C_TONE']
    c_tone_b = population[0].fitnesses['C_TONE_B']
    cadence = population[0].fitnesses['CADENCE']
    l_note = population[0].fitnesses['L_NOTE']
    i_res = population[0].fitnesses['I_RES']
    l_int = population[0].fitnesses['L_INT']
    l_dur = population[0].fitnesses['L_DUR']
    cons_r = population[0].fitnesses['CONS_R']
    cons_n = population[0].fitnesses['CONS_N']
    pattern_d = population[0].fitnesses['PATTERN_D']
    pattern_sd = population[0].fitnesses['PATTERN_SD']
    eq_indiv = proportion_equal_to_highest_fitness(population)

    data = [
        iteration,
        max_fitness,
        min_fitness,
        avg_fitness,
        c_tone,
        c_tone_b,
        cadence,
        l_note,
        i_res,
        l_int,
        l_dur,
        cons_r,
        cons_n,
        pattern_d,
        pattern_sd,
        eq_indiv,
        constants.NUM_OF_MEASURES,
        constants.LEARNING_RATE,
        constants.POPULATION_SIZE,
        constants.ELITISM_SIZE,
        constants.CROSSOVER
    ]

    for i in range(len(data)):
        if isinstance(data[i], float):
            data[i] = round(data[i], 3)
    folder = f'./output/{constants.SYSTEM}/experiment-iterations={constants.ITERATIONS}-pop={constants.POPULATION_SIZE}'
    file = f'/experiment-crossover={constants.CROSSOVER}-{datetime.datetime.now().date()}.csv'

    write_to_csv(data, header, folder, file)


def write_to_csv(data, header, folder, file):
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(folder + file):
        with open(folder + file, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
            writer.writerow(header)
            writer.writerow(data)

    else:
        with open(folder + file, mode='a') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
            writer.writerow(data)


def write_average_runs(converge_it, population: [Individual]):
    fitnesses = list(map(lambda x: x.fitness, population))
    avg_fitness = sum(fitnesses) / len(population)
    max_fitness = max(fitnesses)
    min_fitness = min(fitnesses)

    c_tone = sum(list(map(lambda x: x.fitnesses['C_TONE'], population))) / len(population)
    c_tone_b = sum(list(map(lambda x: x.fitnesses['C_TONE_B'], population))) / len(population)
    cadence = sum(list(map(lambda x: x.fitnesses['CADENCE'], population))) / len(population)
    l_note = sum(list(map(lambda x: x.fitnesses['L_NOTE'], population))) / len(population)
    i_res = sum(list(map(lambda x: x.fitnesses['I_RES'], population))) / len(population)
    l_int = sum(list(map(lambda x: x.fitnesses['L_INT'], population))) / len(population)
    l_dur = sum(list(map(lambda x: x.fitnesses['L_DUR'], population))) / len(population)
    cons_r = sum(list(map(lambda x: x.fitnesses['CONS_R'], population))) / len(population)
    cons_n = sum(list(map(lambda x: x.fitnesses['CONS_N'], population))) / len(population)
    pattern_d = sum(list(map(lambda x: x.fitnesses['PATTERN_D'], population))) / len(population)
    pattern_sd = sum(list(map(lambda x: x.fitnesses['PATTERN_SD'], population))) / len(population)
    eq_indiv = proportion_equal_to_highest_fitness(population)

    data = [
        constants.ITERATIONS,
        converge_it,
        max_fitness,
        min_fitness,
        avg_fitness,
        c_tone,
        c_tone_b,
        cadence,
        l_note,
        i_res,
        l_int,
        l_dur,
        cons_r,
        cons_n,
        pattern_d,
        pattern_sd,
        eq_indiv,
        constants.NUM_OF_MEASURES,
        constants.LEARNING_RATE,
        constants.POPULATION_SIZE,
        constants.ELITISM_SIZE,
        constants.CROSSOVER
    ]

    header = ["I", "I_CONV", "MAX_F", "MIN_F", "MEAN_F", "C_TONE", "C_TONE_B", "CADENCE", "L_NOTE", "I_RES", "L_INT", "L_DUR",
              "CONS_R", "CONS_N", "PATTERN_D", "PATTERN_SD", "EQ_INDIV", "INDIV_SIZE", "L_RATE", "POP_SIZE", "E_SIZE", "X_TYPE"]
    folder = f'./output/{constants.SYSTEM}/{constants.RUN_MODE}-experiment-iterations={constants.ITERATIONS}-pop={constants.POPULATION_SIZE}'
    file = f'/{constants.RUN_MODE}-{constants.SYSTEM}-experiment-crossover={constants.CROSSOVER}-{datetime.datetime.now().date()}.csv'
    write_to_csv(data, header, folder, file)


def write_matrices(pitch_matrix, backoff_matrix, duration_matrix):
    if constants.SYSTEM != "GA":
        folder = f'./output/{constants.SYSTEM}/experiment-iterations={constants.ITERATIONS}-pop={constants.POPULATION_SIZE}'
        pitch_matrix.to_csv(folder + '/pitch_matrix.csv')
        backoff_matrix.to_csv(folder + '/backoff_matrix.csv')
        duration_matrix.to_csv(folder + '/duration_matrix.csv')


def measure_counter(population: [Individual]):
    measures = util.flatten(list(map(lambda x: x.get_notes_per_measure(), population)))
    pitches_per_ind = []

    for m in measures:
        curr_individual = []
        for note in m:
            curr_individual.append(note.pitch)
        curr_individual = tuple(curr_individual)
        pitches_per_ind.append(curr_individual)

    collections.Counter(pitches_per_ind)


def proportion_equal_to_highest_fitness(population: [Individual]):
    individuals = list(map(lambda x: x.get_notes_per_measure(), population))
    highest_fitness_i = None
    counter = 0.0

    for i in range(len(individuals)):
        ind = individuals[i]
        curr_individual = []
        for m in ind:
            for n in m:
                curr_individual.append(n.pitch)
        curr_individual = tuple(curr_individual)
        if i == 0:
            highest_fitness_i = curr_individual
        if curr_individual == highest_fitness_i:
            counter += 1.0
    return counter / len(population)
