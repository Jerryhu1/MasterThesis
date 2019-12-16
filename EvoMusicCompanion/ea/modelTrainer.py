from collections import defaultdict

import collections
import numpy as np
import pandas as pd
from ea import util, individual, constants
import nltk

from music21 import *


def flatten(l):
    return [item for sublist in l for item in sublist]


def train_pitch_matrix(scores):
    if scores is None:
        scores = get_corpus()

    notes = flatten(get_pitches_per_score(scores))

    if constants.N_GRAM == 'trigram':
        matrix = get_trigram_matrix(notes)
    else:
        matrix = get_bigram_matrix(notes)

    return get_probabilistic_matrix(matrix)


def get_trigram_matrix(items):
    trigrams = nltk.trigrams(items)
    matrix = defaultdict(lambda: defaultdict(lambda: 0))
    for n1, n2, n3 in trigrams:
        matrix[(n1, n2)][n3] += 1
    matrix = pd.DataFrame(matrix)
    matrix = matrix.fillna(0)
    return matrix


def get_bigram_matrix(items):
    if items[0] is individual.Note:
        items = map(lambda x: x.pitch, items)
    bigrams = nltk.bigrams(items)
    matrix = defaultdict(lambda: defaultdict(lambda: 0))
    for n1, n2 in bigrams:
        matrix[n1][n2] += 1
    matrix = pd.DataFrame(matrix)
    matrix = matrix.fillna(0)
    return matrix


def get_corpus():
    curr_corpus = corpus.corpora.LocalCorpus('wiki').metadataBundle

    scores = []

    for c in curr_corpus[0:20]:
        score = c.parse()
        # Tranpose to C
        score = util.transpose_piece(score, 'C')
        scores.append(score)

    return scores


def get_pitches_per_score(scores):
    all_notes_per_score = []  # Multidimensional array of all notes per piece

    for p in scores:
        curr_pitches = []
        # Get a part of the piece
        for part in p.parts:
            measure_iterator = part.getElementsByClass(stream.Measure)
            if len(measure_iterator) > 0:
                note_iterator = measure_iterator.flat.notesAndRests
            else:
                note_iterator = part.notesAndRests

            if len(note_iterator) == 0:
                continue

            for el in note_iterator:
                if el.isRest:
                    pitch_name = 'REST'
                else:
                    if el.isChord:
                        root = el.root()
                        if root is None:
                            continue
                        pitch_name = el.root().nameWithOctave
                    else:
                        pitch_name = el.nameWithOctave
                    if pitch_name not in constants.NOTE_RANGE:
                        continue
                    if '-' in pitch_name or '##' in pitch_name:
                        pitch_name = el.pitch.getEnharmonic().nameWithOctave
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


def get_probabilistic_matrix(matrix):
    matrix = matrix.astype(float)
    for n1_n2 in matrix:
        total_count = sum(matrix[n1_n2])
        for n3 in matrix[n1_n2].keys():
            if matrix[n1_n2][n3] != 0.0:
                matrix[n1_n2][n3] /= total_count

    return matrix


def train_duration_matrix(scores):
    if scores is None:
        scores = get_corpus()
    # set containing all possible notes for matrix creation
    possible_durations = ['half', 'quarter', 'eighth', '16th']
    all_durations = []  # Multidimensional array of all notes per piece

    for i in scores:
        # Get a part of the piece
        noteIterator = i.parts[0].getElementsByClass(stream.Measure).flat.getElementsByClass('Note')
        if len(noteIterator) == 0:
            noteIterator = i.parts[0].notesAndRests

        for j in range(len(noteIterator)):
            dur = noteIterator[j]

            if dur.duration.type not in possible_durations:
                continue

            all_durations.append(dur.duration.type)

    if constants.N_GRAM == 'trigram':
        matrix = get_trigram_matrix(all_durations)
    else:
        matrix = get_bigram_matrix(all_durations)

    return get_probabilistic_matrix(matrix)


def train_interval_matrix(scores):
    first_notes_per_bar = []
    all_intervals = []
    for s in scores:
        noteIterator = s.parts[0].getElementsByClass(stream.Measure)
        if len(noteIterator) == 0:
            noteIterator = s.parts[0].notesAndRests.stream()
        for i in noteIterator:
            firstNote = None
            counter = 1
            m = []
            for j in i.notesAndRests:
                if j.isChord:
                    curr_note = note.Note(j.root())
                elif j.isRest:
                    m.append('REST')
                    continue
                else:
                    curr_note = j
                if counter == 1:
                    if j.isChord:
                        firstNote = note.Note(j.root())
                    else:
                        firstNote = j
                    pitch_name = firstNote.nameWithOctave
                    if '-' in pitch_name or '##' in pitch_name:
                        pitch_name = firstNote.pitch.getEnharmonic().nameWithOctave
                    if pitch_name in constants.NOTE_RANGE:
                        first_notes_per_bar.append(pitch_name)
                    counter += 1
                    continue
                octave = curr_note.octave
                root = note.Note('C')
                root.octave = octave
                interv = interval.Interval(root,  curr_note).name
                m.append(interv)
                counter += 1
            all_intervals.append(interv)

    bigrams = list(nltk.bigrams(all_intervals))
    matrix = defaultdict(lambda: defaultdict(lambda: 0))

    for i1,i2 in bigrams:
        matrix[i1][i2] += 1

    for i1 in matrix:
        total = float(sum(matrix[i1].values()))
        for i2 in matrix[i1]:
            matrix[i1][i2] /= total

    int_matrix = pd.DataFrame(matrix)
    int_matrix = int_matrix.fillna(0)
    return int_matrix


def update_matrix(samples, matrix, convergence_rate):
    if constants.N_GRAM == 'trigram':
        n_matrix = get_trigram_matrix(flatten(samples))
    else:
        n_matrix = get_bigram_matrix(flatten(samples))

    u_matrix = get_probabilistic_matrix(n_matrix)
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

            new_matrix[i][j] = matrix[i][j] + (difference * convergence_rate)

    return new_matrix
