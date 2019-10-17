import collections

import numpy as np
import pandas as pd
from music21 import *


def flatten(l):
    return [item for sublist in l for item in sublist]


def train():
    pieces = get_corpus()
    notes = get_notes_per_score(pieces)
    possible_notes = get_possible_notes(flatten(notes))
    freq_array = create_frequency_array(notes)
    freq_matrix = create_frequency_matrix(notes, possible_notes)
    return get_probabilistic_matrix(freq_matrix, freq_array, possible_notes)


def get_possible_notes(notes):
    return set(notes)


def get_corpus():
    six_eight = corpus.search('6/8')

    bach_corpus_scores = []

    for c in six_eight:
        score = c.parse()
        bach_corpus_scores.append(score)

    return bach_corpus_scores


def get_notes_per_score(scores):
    possible_notes = set()  # set containing all possible notes for matrix creation
    all_notes_per_score = []  # Multidimensional array of all notes per piece

    for p in scores:
        curr_notes = []
        # Get a part of the piece
        note_iterator = p.parts[0].getElementsByClass(stream.Measure).flat.getElementsByClass('Note')
        if len(note_iterator) == 0:
            continue
        for el in note_iterator:
            pitch_name = el.nameWithOctave
            if '-' in pitch_name or '##' in pitch_name:
                note_name = el.pitch.getEnharmonic().nameWithOctave
                possible_notes.add(note_name)
                curr_notes.append(note_name)
            else:
                note_name = el.nameWithOctave
                possible_notes.add(note_name)
                curr_notes.append(note_name)
        all_notes_per_score.append(curr_notes)

    return all_notes_per_score, possible_notes


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


def update_matrix(samples, matrix, divergence_rate):

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
