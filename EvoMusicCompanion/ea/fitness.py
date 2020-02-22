import collections

from music21 import pitch, interval, scale

from ea import util, constants
from ea.individual import Individual, Note
from nltk import ngrams
import math
import time
import threading

major_scale = ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5']


def print_fitness_values(individual):
    int_pattern = intervallic_patterns(individual)
    chord_tone_beat = fitness_chord_tone_beat(individual)
    chord_tone = fitness_chord_tone(individual)
    last_note = cadence(individual)
    long_note = long_notes(individual)
    duration = duration_patterns(individual)
    duration_change = duration_changes(individual)
    intervals = interval_size(individual)
    rests = consecutive_rests(individual)
    interval_resolution = interval_resolution_strong_beat(individual)
    consecutive_notes = similar_notes(individual)

    total = get_fitness(individual)
    print(f'Interval pattern fitness: {int_pattern}')
    print(f'Duration pattern fitness: {duration}')
    print(f'Chord tone beat fitness: {chord_tone_beat}')
    print(f'Chord tone fitness: {chord_tone}')
    print(f'Last note fitness: {last_note}')
    print(f'Long note fitness: {long_note}')
    print(f'Interval size fitness: {intervals}')
    print(f'Consecutive rests fitness: {rests}')
    print(f'Interval resolution fitness: {interval_resolution}')
    print(f'duration change fitness: {duration_change}')
    print(f'Consecutive notes fitness: {consecutive_notes}')
    print(f'Total fitness in indiv: {individual.fitness}')
    print(f'Total fitness: {total}')


w1 = 1.0
w2 = 1.0
w3 = 1.0
w4 = 1.0
w5 = 1.0
w6 = 1.0
w7 = 1.0
w8 = 1.0


def get_fitness(individual):
    int_pattern = intervallic_patterns(individual)
    duration = duration_patterns(individual)
    chord_tone_beat = fitness_chord_tone_beat(individual)
    chord_tone = fitness_chord_tone(individual)
    last_note = cadence(individual)
    long_note = long_notes(individual)
    duration_change = duration_changes(individual)
    intervals = interval_size(individual)
    rests = consecutive_rests(individual)
    interval_resolution = interval_resolution_strong_beat(individual)
    consecutive_notes = similar_notes(individual)

    dic = {
        "C_TONE" : chord_tone,
        "C_TONE_B": chord_tone_beat,
        "CADENCE": last_note,
        "L_NOTE": long_note,
        "I_RES": interval_resolution,
        "L_INT": intervals,
        "L_DUR": duration_change,
        "CONS_R": rests,
        "CONS_N": consecutive_notes,
        "PATTERN_D": duration,
        "PATTERN_SD": int_pattern
    }

    return (int_pattern + chord_tone + chord_tone_beat + last_note + long_note + duration + intervals + rests + \
           interval_resolution + duration_change + consecutive_notes), dic

def set_fitness(individual):
    f, dic = get_fitness(individual)
    individual.fitness = f
    individual.fitnesses = dic


def set_fitness_for_population(population: [Individual]):
    for i in population:
        set_fitness(i)
    return population


def get_distance(i1: Individual, i2: Individual):
    dic = {
        "C_TONE" : 0.0,
        "C_TONE_B": 0.0,
        "CADENCE": 0.0,
        "L_NOTE": 0.0,
        "I_RES": 0.0,
        "L_INT": 0.0,
        "L_DUR": 0.0,
        "CONS_R": 0.0,
        "CONS_N": 0.0,
        "PATTERN_D": 0.0,
        "PATTERN_SD": 0.0
    }

    for k, v in i1.fitnesses.items:
        i2_val = i2.fitnesses[k]

        delta = abs(v - i2_val)
        dic[k] = delta

    return sum(dic.values()), dic


def long_notes(individual: Individual):
    measures = individual.measures
    fitness = 0
    long_note_counter = 0.0

    for m in measures:
        for n in m.notes:
            duration_name = n.duration.duration_name
            if duration_name == 'quarter' or duration_name == 'half':
                long_note_counter += 1.0
                if n.pitch == 'REST':
                    fitness -= 1.0
                elif n.pitchWithoutOctave in m.chordWithoutOctave:
                    fitness += 1.0
                else:
                    fitness -= 0.5
    if long_note_counter == 0 or fitness == 0:
        return 0.0
    return fitness / long_note_counter


def consecutive_rests(individual: Individual):
    measures = individual.measures
    fitness = 0
    for m in measures:
        counter = 0.0
        for n in range(len(m.notes)):
            note = m.notes[n]
            duration_value = m.notes[n].duration.duration_value
            if note.pitch == 'REST':
                counter += duration_value

            if n == len(m.notes) - 1 or note.pitch != 'REST':
                if counter >= 0.5:
                    fitness -= 1.0
                counter = 0.0

    return fitness / len(measures)


def interval_resolution_strong_beat(individual):
    score = 0
    divider_counter = 0
    measures = individual.measures
    strong_beats = [0.0, 0.5]
    prev_measure_note = None

    for i in range(len(measures)):
        m = measures[i]
        dur_counter = 0.0
        for j in range(-1, len(m.notes)):
            if j == len(m.notes) - 1:
                prev_measure_note = m.notes[j]
                continue
            if prev_measure_note is not None and j == -1:
                n1 = prev_measure_note
                n2 = m.notes[j]
            elif j == -1 and prev_measure_note is None:
                continue
            else:
                n1 = m.notes[j]
                n2 = m.notes[j + 1]
                dur_counter += n1.duration.duration_value

            if n1.pitch == "REST" or n2.pitch == "REST":
                continue

            # Strong beat, resolve
            if dur_counter in strong_beats:
                p1 = pitch.Pitch(n1.pitchWithoutOctave)
                p2 = pitch.Pitch(n2.pitchWithoutOctave)

                root = pitch.Pitch('C')
                i1 = interval.Interval(root, p1)
                i2 = interval.Interval(root, p2)

                divider_counter += 1
                if i1.name == 'M2' and i2.name == 'P1':
                    score += 1.0
                elif i1.name == 'P4' and i2.name == 'M3':
                    score += 1.0
                elif i1.name == 'M6' and i2.name == 'P5':
                    score += 0.5
                elif i1.name == 'M7' and i2.name == 'P1':
                    score += 1.0
                elif i1.name == 'M3' and i2.name == 'P1':
                    score += 0.5

    if divider_counter == 0.0:
        return 0.0
    return score / (2 * len(individual.measures) - 1)


def interval_size(individual):
    score = 0
    notes: [Note] = individual.get_flattened_notes()

    for i in range(1, len(notes)):
        if notes[i - 1].pitch == 'REST' or notes[i].pitch == 'REST':
            continue
        n1 = notes[i - 1].to_music21_note()
        n2 = notes[i].to_music21_note()

        i1 = interval.Interval(n1, n2)
        if i1.semitones >= 9:
            score -= 1.0
    if score == 0.0:
        return 0.0
    return score / (len(notes) - 1)


def fitness_chord_tone_beat(individual: Individual):
    strong_beat = [0.0, 0.5]
    score = 0.0
    for m in individual.measures:
        dur_counter = 0.0
        for n in m.notes:
            if dur_counter in strong_beat:
                if n.pitchWithoutOctave in m.chordWithoutOctave:
                    score += 1.0
                else:
                    score -= 1.0
            dur_counter += n.duration.duration_value
    # 2 strong beats per measure
    if score == 0.0:
        return 0.0
    if score / (2*len(individual.measures)) == 1.0 and individual.measures[0].notes[0].pitch == 'REST':
        print('Rest in chord tone')
    return score / (2*len(individual.measures))


def fitness_chord_tone(individual: Individual):
    total_count = 0.0
    for j in individual.measures:
        counter = 0.0
        chord = j.chordWithoutOctave
        for n in j.notes:
            if n.pitchWithoutOctave in chord:
                counter += 1.0
        total_count += counter / len(j.notes)
    if total_count == 0.0:
        return 0.0
    return total_count / len(individual.measures)


def cadence(individual: Individual):
    last_measure = individual.measures[-1]
    strong_beats = [0.0, 0.5]
    dur_counter = 0.0
    for i in range(len(last_measure.notes)):
        note = last_measure.notes[i]
        if i == len(last_measure.notes) - 1:
            if note.pitchWithoutOctave == last_measure.chordWithoutOctave[0]:
                if dur_counter in strong_beats:
                    if note.duration.duration_value > 0.25:
                        return 1.0
                    else:
                        return 0.5
                else:
                    return 0.5
            else:
                return -1.0
        dur_counter += last_measure.notes[i].duration.duration_value

    return -1.0


def intervallic_patterns(individual: Individual):
    notes: [Note] = individual.get_flattened_notes()
    notes = list(filter(lambda x: x.pitch != 'REST', notes))
    intervals = []
    for i in range(1, len(notes)):
        n1 = notes[i - 1].to_music21_note()
        n2 = notes[i].to_music21_note()
        n1_scalestep = get_scale_position(n1.nameWithOctave)
        n2_scalestep = get_scale_position(n2.nameWithOctave)
        scalestep_interval = n2_scalestep - n1_scalestep
        intervals.append(scalestep_interval)
    pattern_length_counter = find_patterns(intervals)
    fitness = 0.0
    for k, v in pattern_length_counter.items():
        # Maximum number of k length patterns in piece
        divider = len(notes) - k + 1
        fitness += v / divider
    if fitness == 0.0:
        return 0.0
    return fitness / len(pattern_length_counter.items())


def get_scale_position(p):
    if p in constants.C_MAJOR_SCALE:
        return constants.C_MAJOR_SCALE.index(p)
    return -1


def duration_changes(individual: Individual):
    notes = individual.get_flattened_notes()
    durations = list(map(lambda x: x.duration.duration_value, notes))
    counter = 0
    for i in range(1, len(durations)):
        d_1 = durations[i - 1]
        d_2 = durations[i]

        if d_1 / d_2 >= 4.0:
            counter += 1

    return - (counter / (len(notes) - 1))


def duration_patterns(individual: Individual):
    notes = individual.get_flattened_notes()
    durations = list(map(lambda x: x.duration.duration_name, notes))

    pattern_counter = find_patterns(durations)
    fitness = 0.0
    for k, v in pattern_counter.items():
        divider = len(notes) - k + 1

        fitness += v / divider
    if fitness == 0.0:
        return 0.0
    return fitness / len(pattern_counter.items())


def similar_notes(individual: Individual):
    notes_per_measure = individual.get_notes_per_measure()
    fitness = 0.0
    for m in notes_per_measure:
        consecutive_notes_count = 0
        prev_note = m[0].pitch
        for i in range(1,len(m)):
            curr_note = m[i].pitch
            if prev_note == curr_note:
                consecutive_notes_count += 1
            prev_note = curr_note
        fitness -= consecutive_notes_count / len(m)
    return fitness / len(individual.measures)


def find_patterns(sequence):
    min_pattern_length = 3
    max_pattern_length = 7
    min_support_count = 2
    k = min_pattern_length
    pattern_length_counter = collections.defaultdict(lambda: 0)

    while k <= max_pattern_length:
        grams = ngrams(sequence, k)
        counter = collections.Counter(grams)
        for key, v in counter.items():
            if v >= min_support_count:
                pattern_length_counter[k] += v
        k += 1
    return pattern_length_counter


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
