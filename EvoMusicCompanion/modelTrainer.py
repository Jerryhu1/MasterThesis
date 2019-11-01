import collections

import numpy as np
import pandas as pd
from music21 import *


def flatten(l):
    return [item for sublist in l for item in sublist]


def train_pitch_matrix(scores):
    if scores is None:
        scores = get_corpus()
    notes = get_pitches_per_score(scores)
    possible_pitches = get_possible_pitches(flatten(notes))
    freq_array = create_frequency_array(notes)
    freq_matrix = create_frequency_matrix(notes, possible_pitches)
    return get_probabilistic_matrix(freq_matrix, freq_array, possible_pitches)


def get_possible_pitches(notes):
    return set(notes)


def get_corpus():
    six_eight = corpus.search('6/8')

    bach_corpus_scores = []

    for c in six_eight:
        score = c.parse()
        bach_corpus_scores.append(score)

    return bach_corpus_scores


def get_pitches_per_score(scores):
    all_notes_per_score = []  # Multidimensional array of all notes per piece

    for p in scores:
        curr_pitches = []
        # Get a part of the piece
        measure_iterator = p.parts[0].getElementsByClass(stream.Measure)
        if len(measure_iterator) > 0:
            note_iterator = measure_iterator.flat.getElementsByClass('Note')
        else:
            note_iterator = p.parts[0].getElementsByClass('Note')

        if len(note_iterator) == 0:
            continue
        
        for el in note_iterator:
            pitch_name = el.nameWithOctave
            if '-' in pitch_name or '##' in pitch_name:
                pitch_name = el.pitch.getEnharmonic().nameWithOctave
                curr_pitches.append(pitch_name)
            else:
                curr_pitches.append(pitch_name)
        all_notes_per_score.append(curr_pitches)

    return all_notes_per_score


def create_frequency_array(notes):
    # Get frequency array
    counter = collections.Counter(flatten(notes))
    # Initial note counter
    counter[' '] = len(notes)
    return counter


def create_frequency_matrix(pieces, possible_notes):
    """
        Creates the frequency matrix, pieces must be supplied as multi dimensional array of notes, each
        entry is one piece
    """
    possible_notes.add(' ')
    zeros = np.full((len(possible_notes), len(possible_notes)), 0)
    matrix = pd.DataFrame(zeros, index=possible_notes, columns=possible_notes)
    matrix = matrix.astype(float)
    for n in pieces:
        # Fill transition matrix frequencies
        for i in range(len(n) + 1):
            # Last note
            curr_note = n[i - 1]
            if i == len(n):
                matrix[curr_note][' '] = matrix[curr_note][' '] + 1
                continue
            # First note
            next_note = n[i]
            if i == 0:
                matrix[' '][next_note] = matrix[' '][next_note] + 1
                continue
            matrix[curr_note][next_note] = matrix[curr_note][next_note] + 1

    return matrix


def get_probabilistic_matrix(matrix, frequency_array, possible_notes):
    # Divide each row to get probabilistic model
    for i in possible_notes:
        for j in possible_notes:
            matrix[j][i] = matrix[j][i] / frequency_array[j]
    return matrix


def train_duration_matrix(scores):
    if scores is None:
        scores = get_corpus()
    # set containing all possible notes for matrix creation
    possible_durations = ['half', 'quarter', 'eighth', '16th', '32nd', '64th']
    all_durations = []  # Multidimensional array of all notes per piece
    last_durations = []

    for i in scores:
        # Get a part of the piece
        noteIterator = i.parts[0].getElementsByClass(stream.Measure).flat.getElementsByClass('Note')
        curr_duration = []

        if len(noteIterator) == 0:
            continue
        for j in range(len(noteIterator)):
            dur = noteIterator[j]

            if dur.duration.type not in possible_durations:
                continue

            if j == len(noteIterator)-1:
                last_durations.append(dur.duration.type)

            curr_duration.append(dur.duration.type)

        all_durations.append(curr_duration)

    last_durations_counter = collections.Counter(last_durations)

    counter = collections.Counter(flatten(all_durations))
    counter = counter - last_durations_counter

    zeros = np.full((len(possible_durations), len(possible_durations)), 0)
    matrix = pd.DataFrame(zeros, index=possible_durations, columns=possible_durations)
    matrix = matrix.astype(float)

    # Fill transition matrix frequencies
    for dur in all_durations:
        for j in range(len(dur)):
            # First note
            if j == 0:
                continue

            curr_duration = dur[j-1]
            next_duration = dur[j]

            matrix[curr_duration][next_duration] = matrix[curr_duration][next_duration] + 1

    # Divide each row to get probabilistic model
    for i in possible_durations:
        for j in possible_durations:
            if counter[j] != 0 and matrix[j][i] != 0:
                matrix[j][i] = matrix[j][i] / counter[j]

    return matrix


def update_pitch_matrix(samples, matrix, divergence_rate):

    possible_notes = set(flatten(samples))
    freq_array = create_frequency_array(samples)
    freq_matrix = create_frequency_matrix(samples, possible_notes)
    u_matrix = get_probabilistic_matrix(freq_matrix, freq_array, possible_notes)
    new_matrix = matrix.copy()

    for i in new_matrix.keys():
        for j in new_matrix.keys():

            if i in u_matrix and j in u_matrix[i]:
                # u_matrix contains the values, subtract from each other
                difference = u_matrix[i][j] - matrix[i][j]
            elif i not in u_matrix:
                # u_matrix does not contain the column, we can not update transitions strating from this note
                difference = 0.0
            else:  # u_matrix contains the column, but not the row. So no transitions to that note at all
                difference = -matrix[i][j]

            new_matrix[i][j] = matrix[i][j] + (difference * divergence_rate)

    return new_matrix
