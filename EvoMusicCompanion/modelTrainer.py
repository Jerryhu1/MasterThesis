from music21 import *
import collections
import numpy as np
import pandas as pd
import gzip
import random


def flatten(l):
    return [item for sublist in l for item in sublist]


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
    counter = notes
    # Initial note counter
    counter[' '] = len(notes)
    return counter


def create_frequency_matrix(notes, possible_notes):
    possible_notes.add(' ')
    zeros = np.full((len(possible_notes), len(possible_notes)), 0)
    matrix = pd.DataFrame(zeros, index=possible_notes, columns=possible_notes)
    matrix = matrix.astype(float)

    for n in notes:
        # Fill transition matrix frequencies
        for i in range(len(n) + 1):
            # First note
            next_note = n[i]
            if i == 0:
                matrix[' '][next_note] = matrix[' '][next_note] + 1
                continue
            # Last note
            curr_note = n[i - 1]
            if i == len(n):
                matrix[curr_note][' '] = matrix[curr_note][' '] + 1
                continue

            matrix[curr_note][next_note] = matrix[curr_note][next_note] + 1
    return matrix


def get_probabilistic_matrix(matrix, frequency_array, possible_notes):
    # Divide each row to get probabilistic model
    for i in possible_notes:
        for j in possible_notes:
            matrix[j][i] = matrix[j][i] / frequency_array[j]
    return matrix


def update_matrix(samples, matrix):

    notes = get_notes_per_score(samples)
    possible_notes = set(flatten(notes))
    freq_array = create_frequency_array(samples)
    freq_matrix = create_frequency_matrix(notes, possible_notes)

    u_matrix = get_probabilistic_matrix(freq_matrix, freq_array, possible_notes)

    error_matrix = u_matrix - matrix
