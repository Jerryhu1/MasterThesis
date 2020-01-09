import collections

from music21 import pitch, interval

from ea import util
from ea.individual import Individual, Note
from nltk import ngrams

major_scale = ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5']


def print_fitness_values(individual):
    int_pattern = intervallic_patterns(individual)
    chord_tone_beat = fitness_chord_tone_beat(individual)
    chord_tone = fitness_chord_tone(individual)
    last_note = last_note_closure(individual)
    long_note = long_notes(individual)
    duration = duration_patterns(individual)
    intervals = interval_size(individual)
    rests = consecutive_rests(individual)
    interval_resolution = interval_resolution_strong_beat(individual)

    print(f'Interval pattern fitness: {int_pattern}')
    print(f'Duration pattern fitness: {duration}')
    print(f'Chord tone beat fitness: {chord_tone_beat}')
    print(f'Chord tone fitness: {chord_tone}')
    print(f'Last note fitness: {last_note}')
    print(f'Long note fitness: {long_note}')
    print(f'Interval size fitness: {intervals}')
    print(f'Consecutive rests fitness: {rests}')
    print(f'Interval resolution fitness: {interval_resolution}')
    print(f'Total fitness: {individual.fitness}')


w1 = 0.5
w2 = 0.5
w3 = 1.0
w4 = 1.0
w5 = 1.0
w6 = 1.0
w7 = 1.0
w8 = 1.0


def get_fitness(individual):
    int_pattern = intervallic_patterns(individual)
    chord_tone_beat = fitness_chord_tone_beat(individual)
    chord_tone = fitness_chord_tone(individual)
    last_note = last_note_closure(individual)
    long_note = long_notes(individual)
    duration = duration_patterns(individual)
    intervals = interval_size(individual)
    rests = consecutive_rests(individual)
    interval_resolution = interval_resolution_strong_beat(individual)

    return int_pattern + chord_tone + chord_tone_beat + last_note + long_note + duration + intervals + rests + interval_resolution


def set_fitness(individual):
    individual.fitness = get_fitness(individual)


def set_fitness_for_population(population: [Individual]):
    for i in population:
        set_fitness(i)
    return population


def long_notes(individual: Individual):
    measures = individual.measures
    fitness = 0
    for m in measures:
        measure_fitness = 0.0
        long_note_counter = 0.0
        for n in m.notes:
            duration_name = n.duration.duration_name
            if duration_name == 'quarter' or duration_name == 'half':
                long_note_counter += 1.0
                if n.pitch == 'REST':
                    measure_fitness -= 1.0
                if n.pitchWithoutOctave in m.chordWithoutOctave:
                    measure_fitness += 1.0
                else:
                    measure_fitness -= 1.0
        if long_note_counter == 0:
            continue
        fitness += (measure_fitness / long_note_counter)
    return fitness / len(individual.measures)


def consecutive_rests(individual: Individual):
    measures = individual.measures
    fitness = 0
    divider = 0.0
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
    for m in individual.measures:
        strong_beats = [0.0, 0.75]
        dur_counter = 0.0
        for i in range(1, len(m.notes)):
            if m.notes[i-1].pitch == 'REST' or m.notes[i].pitch == 'REST':
                continue
            divider_counter += 1
            dur_counter += m.notes[i-1].duration.duration_value

            n1 = pitch.Pitch(m.notes[i - 1].pitchWithoutOctave)
            n2 = pitch.Pitch(m.notes[i].pitchWithoutOctave)
            root = pitch.Pitch('C')
            i1 = interval.Interval(root, n1)
            i2 = interval.Interval(root, n2)
            # Strong beat, resolve
            if dur_counter in strong_beats:
                if i1.name == 'M2' and i2.name == 'P1':
                    score += 2.0
                elif i1.name == 'P4' and i2.name == 'M3':
                    score += 2.0
                elif i1.name == 'M6' and i2.name == 'P5':
                    score += 1.0
                elif i1.name == 'M7' and i2.name == 'P1':
                    score += 2.0
                elif i1.name == 'M3' and i2.name == 'P1':
                    score += 1.0
    return score / divider_counter


def interval_size(individual):

    score = 0
    notes: [Note] = individual.get_flattened_notes()

    for i in range(1, len(notes)):
        if notes[i-1].pitch == 'REST' or notes[i].pitch == 'REST':
            continue
        n1 = notes[i - 1].to_music21_note()
        n2 = notes[i].to_music21_note()

        i1 = interval.Interval(n1, n2)
        if i1.semitones >= 9:
            score -= 1.0
    return score / (len(notes) / 2.0)


def fitness_chord_tone_beat(individual: Individual):
    strong_beat = [0.0, 0.5]
    score = 0
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
    return (score / 2) / len(individual.measures)


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


def last_note_closure(individual: Individual):
    last_note = individual.measures[-1].notes[-1]
    last_pitch = last_note.pitchWithoutOctave
    last_chord = individual.measures[-1].chordWithoutOctave
    score = 0
    if last_pitch == last_chord[0]:
        if last_note.duration.duration_value > 0.25:
            score += 1.0
        else:
            score += 0.5

    return score


def intervallic_patterns(individual: Individual):
    notes: [Note] = individual.get_flattened_notes()
    notes = list(filter(lambda x: x.pitch != 'REST', notes))
    intervals = []

    for i in range(1, len(notes)):
        n1 = notes[i - 1].to_music21_note()
        n2 = notes[i].to_music21_note()
        i1 = interval.Interval(n1, n2)
        intervals.append(i1.name)

    pattern_length_counter = find_patterns(intervals)
    fitness = 0.0
    for k, v in pattern_length_counter.items():
        score = 0.0
        if k == 3:
            score = 3.0
        elif k == 4:
            score = 4.0
        elif k == 5:
            score = 5.0
        elif k == 6:
            score = 6.0
        elif k == 7:
            score = 7.0
        # Max of N bars x 16th notes in piece
        max_notes = len(individual.measures) * 16
        divider = max_notes / k
        fitness += (score * v) / divider

    return fitness


def duration_patterns(individual: Individual):
    notes = individual.get_flattened_notes()
    durations = list(map(lambda x: x.duration.duration_name, notes))

    pattern_counter = find_patterns(durations)
    fitness = 0.0
    for k, v in pattern_counter.items():
        score = 0.0
        if k == 4:
            score = 4.0
        elif k == 5:
            score = 5.0
        elif k == 6:
            score = 6.0
        elif k == 7:
            score = 7.0
        max_notes = len(individual.measures) * 16
        divider = max_notes / k
        fitness += (score * v) / divider
    if fitness == 0.0:
        return 0.0
    return fitness / len(notes)


def find_patterns(sequence):
    min_pattern_length = 4
    max_pattern_length = 7
    min_support_count = 2
    k = min_pattern_length
    pattern_length_counter = collections.defaultdict(lambda: 0)

    while k <= max_pattern_length:
        grams = ngrams(sequence, k)
        counter = collections.Counter(grams)
        for key, v in counter.items():
            if v > min_support_count:
                pattern_length_counter[k] += 1
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
