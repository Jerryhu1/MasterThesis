from collections import defaultdict

from music21 import pitch, interval
import random
import nltk
import pandas as pd
import os.path

symbol_matrix_path = './symbol_matrix.csv'


def get_symbol_matrix(pitches):

    if os.path.exists(symbol_matrix_path):
        return pd.read_csv(symbol_matrix_path, index_col=0)

    symbols = []

    for s in pitches:
        curr_symbols = []
        for i in range(2, len(s)):
            n1 = pitch.Pitch(s[i - 2])
            n2 = pitch.Pitch(s[i - 1])
            n3 = pitch.Pitch(s[i])

            impl_interval = n2.midi - n1.midi
            real_interval = n3.midi - n2.midi

            is_same_direction = (0 >= impl_interval >= real_interval) \
                                or (0 <= impl_interval <= real_interval)
            is_small_impl_interval = abs(impl_interval) <= 5
            is_small_real_interval = abs(real_interval) <= 5
            # Small impl_interval
            if is_small_impl_interval:

                # small real_interval
                if is_small_real_interval:

                    # Unchanging direction
                    if is_same_direction:
                        new_symbol = "PV"
                    # Changing direction
                    else:
                        if n1 == n3:
                            new_symbol = "QE"
                        else:
                            new_symbol = "QV"
                # Large real_interval
                else:
                    # Unchanging direction
                    if is_same_direction:
                        new_symbol = "PR"
                    # Changing direction
                    else:
                        new_symbol = "QR"
            # Large impl_interval
            else:
                # small real_interval
                if is_small_real_interval:
                    # Unchanging direction
                    if is_same_direction:
                        new_symbol = "PF"
                    # Changing direction
                    else:
                        if n1 == n3:
                            new_symbol = "QE"
                        else:
                            new_symbol = "QF"
                # Large real_interval
                else:
                    # Unchanging direction
                    if is_same_direction:
                        new_symbol = "PL"
                    # Changing direction
                    else:
                        new_symbol = "QL"
            curr_symbols.append(new_symbol)
        symbols.append(curr_symbols)

    bigrams = list(nltk.bigrams(symbols))
    matrix = defaultdict(lambda: defaultdict(lambda: 0))

    for i1, i2 in bigrams:
        matrix[i1][i2] += 1

    for i1 in matrix:
        total = float(sum(matrix[i1].values()))
        for i2 in matrix[i1]:
            matrix[i1][i2] /= total

    pd_matrix = pd.DataFrame(matrix)
    pd_matrix = pd_matrix.fillna(0)
    return pd_matrix


def sample_by_symbol(interval_size, direction, prev_note, matrix):
    i = interval.Interval()
    intervals = []
    if interval_size == 'S':
        if direction == 'UP':
            r = range(0, 6)
        else:
            r = range(0, -6, -1)
    else:
        if direction == 'UP':
            r = range(6, 11)
        else:
            r = range(-6, -11, -1)

    for i in r:
        i = interval.Interval(i)
        inter = get_normal_pitch_name(i.transposePitch(pitch.Pitch(prev_note)))
        intervals.append(inter)
    return sample_random_pitch(matrix, intervals, prev_note)


def get_normal_pitch_name(pitch):
    pitch_name = pitch.nameWithOctave
    if '-' in pitch_name or '##' in pitch_name:
        return pitch.getEnharmonic().nameWithOctave
    else:
        return pitch_name


def sample_random_pitch(matrix, intervals, prev_note):
    total_count = 0
    m = defaultdict(lambda: defaultdict(lambda: 0))
    # Get the intervals and create a distribution
    for i in intervals:
        if i not in matrix[prev_note]:
            continue
        p = matrix[prev_note][i]
        # Create a temporary matrix saving the P and also sum up all probabilities
        m[prev_note][i] = p
        total_count += p

    # Normalize probabilities
    for i in intervals:
        m[prev_note][i] /= total_count

    # Select note in the constrained space
    p_sum = 0
    rng = random.random()
    for i in intervals:
        v = m[prev_note][i]
        if p_sum < rng < p_sum + v:
            return i
        else:
            p_sum += v
