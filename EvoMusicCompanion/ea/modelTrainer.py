from collections import defaultdict

import numpy as np
import pandas as pd
import os.path
from ea import util, individual, constants
import nltk
import csv

from music21 import *

trigram_pitch_matrix_path = './EvoMusicCompanion/trigram_pitch_matrix.csv'
bigram_pitch_matrix_path = './EvoMusicCompanion/bigram_pitch_matrix.csv'
duration_matrix_path = './EvoMusicCompanion/duration_matrix.csv'
symbol_matrix_path = './symbol_matrix.csv'


def flatten(l):
    return [item for sublist in l for item in sublist]


def train_pitch_matrix(scores):

    if constants.N_GRAM == 'bigram':
        if os.path.exists(bigram_pitch_matrix_path):
            return pd.read_csv(bigram_pitch_matrix_path, index_col=0)
    else:
        if os.path.exists(trigram_pitch_matrix_path):
            return read_trigram()
        else:
            print('Could not find trigram path')
    if scores is None:
        scores = get_corpus()

    notes = flatten(get_pitches_per_score(scores))

    if constants.N_GRAM == 'trigram':
        matrix = get_trigram_matrix(notes)
    else:
        matrix = get_bigram_matrix(notes)

    matrix = get_probabilistic_matrix(matrix)
    #matrix.to_csv(pitch_matrix_path)
    return matrix


def get_backoff_matrix():
    return pd.read_csv(bigram_pitch_matrix_path, index_col=0)


def read_trigram():
    with open(trigram_pitch_matrix_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        first_row = []
        second_row = []
        matrix = defaultdict(lambda: defaultdict(lambda: 0))

        for row in csv_reader:
            curr_col = None
            for j in range(len(row)):
                if line_count == 0:
                    if j == 0:
                        first_row.append(None)
                    else:
                        first_row.append(row[j])
                    continue
                elif line_count == 1:
                    if j == 0:
                        second_row.append(None)
                    else:
                        second_row.append(row[j])
                    continue
                if j == 0:
                    curr_col = row[j]
                else:
                    matrix[(first_row[j], second_row[j])][curr_col] = float(row[j])
            line_count += 1

    return pd.DataFrame(matrix)



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
    curr_corpus = corpus.corpora.LocalCorpus('wiki')
    curr_corpus = curr_corpus.metadataBundle

    scores = []

    for c in curr_corpus[0:100]:
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
        if p is None:
            continue
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
                    if el.duration.type == 'whole':
                        continue
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

    if os.path.exists(duration_matrix_path):
        return pd.read_csv(duration_matrix_path, index_col=0)
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

    matrix = get_probabilistic_matrix(matrix)
    matrix.to_csv(duration_matrix_path)
    return matrix
