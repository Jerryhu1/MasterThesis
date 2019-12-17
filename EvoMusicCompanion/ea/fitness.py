from music21 import pitch, interval

from ea import util
from ea.individual import Individual, Note

major_scale = ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5']


def set_fitness(individual):
    individual.fitness = (
            (narmour(individual))
            + fitness_chord_tone_beat(individual)
            + fitness_chord_tone(individual)
            + last_note_closure(individual)
    )


def set_fitness_for_population(population: [Individual]):
    for i in population:
        set_fitness(i)

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


def last_note_closure(individual: Individual):
    last_pitch = individual.measures[-1].notes[-1].pitchWithoutOctave
    last_chord = individual.measures[-1].chordWithoutOctave
    if last_pitch == last_chord:
        return 1
    return 0


def intervallic_patterns(individual: Individual):
    notes: [Note] = individual.get_flattened_notes()
    for i in range(1, len(notes)):
        n1 = notes[i-1].to_music21_note()
        n2 = notes[i].to_music21_note()
        i1 = interval.Interval(n1, n2)





def sign(x):
    if x < 0:
        return -1
    if x == 0:
        return 0
    if x > 0:
        return 1




def narmour(individual: Individual):
    notes = util.flatten(map(lambda x: x.notes, individual.measures))
    pitches = map(lambda x: x.pitch, notes)
    pitches = list(filter(lambda x: x != 'REST', pitches))
    fitness = 0
    for i in range(2, len(pitches)):
        n1 = pitch.Pitch(pitches[i - 2])
        n2 = pitch.Pitch(pitches[i - 1])
        n3 = pitch.Pitch(pitches[i])

        impl_interval = n2.midi - n1.midi
        real_interval = n3.midi - n2.midi
        fitness += registral_direction(impl_interval, real_interval) \
                   + int_diff(impl_interval, real_interval) \
                   + closure(impl_interval, real_interval) \
                   + registral_return(impl_interval, real_interval) \
                   + proximity(real_interval)
    return fitness / len(pitches)


# Small intervals imply a continuation in pitch direction
# Large intervals imply a change of direction
def registral_direction(impl_int, real_int):
    # If small interval
    if impl_int <= 6 and sign(impl_int) == sign(real_int):
        return 1
    if impl_int > 6 and sign(impl_int) != sign(real_int):
        return 1
    return 0


def int_diff(impl_int, real_int):
    # Small interval implies small interval, with diff contour
    if impl_int < 6 \
            and sign(impl_int) == sign(real_int) \
            and abs(impl_int - real_int) < 3:
        return 1
    if impl_int < 6 \
            and sign(impl_int) != sign(real_int) \
            and abs(impl_int - real_int) < 4:
        return 1
    if impl_int > 6 and impl_int >= real_int:
        return 1
    # Give three equal notes a worse score
    if impl_int == real_int:
        return -2
    return 0


def registral_return(impl_int, real_int):
    if abs(impl_int - real_int) <= 2:
        return 1
    return 0


def closure(impl_int, real_int):
    # Changes direction and
    if sign(impl_int) != sign(real_int) and abs(impl_int) - abs(real_int) > 2:
        return 2
    if sign(impl_int) != sign(real_int) and abs(impl_int) - abs(real_int) < 3:
        return 1
    if sign(impl_int) == sign(real_int) and abs(impl_int) - abs(real_int) > 3:
        return 1
    return 0


def proximity(real_int):
    real_int = abs(real_int)
    if real_int >= 6:
        return 0
    if 3 >= real_int <= 5:
        return 1
    if 0 >= real_int <= 2:
        return 1
    return 0
