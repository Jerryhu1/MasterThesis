import constants

from individual import Individual

major_scale = ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5']


def get_fitness(individual):
    notes = [item for sublist in individual.notes for item in sublist]

    counter = 0
    for note in notes:
        if note in major_scale:
            counter += 1

    return counter / len(notes)


def set_fitness(population: [Individual]):
    for i in population:
        i.fitness = fitness_chord_tone_beat(i) + fitness_chord_tone(i)

    return population


def fitness_chord_tone_beat(individual: Individual):
    strong_beat = [0.0, 0.25, 0.5, 0.75]
    score = 0
    for m in individual.measures:
        dur_counter = 0.0
        for n in m.notes:
            if n.pitchWithoutOctave in m.chordWithoutOctave:
                if dur_counter in strong_beat:
                    score += 1
            dur_counter += n.duration.duration_value

    return score / 4


def fitness_chord_tone(individual: Individual):
    total_count = 0.0
    for j in individual.measures:
        counter = 0.0
        chord = j.chordWithoutOctave
        for n in j.notes:
            if n.pitchWithoutOctave in chord:
                counter += 1.0 / len(j.notes)
        j.fitness = counter
        total_count += counter
    return total_count / len(individual.measures)
