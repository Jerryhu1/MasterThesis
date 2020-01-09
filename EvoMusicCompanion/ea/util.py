from music21 import interval, converter, pitch, note


def transpose_piece(piece, key):
    k = piece.analyze('key')
    i = interval.Interval(k.tonic, pitch.Pitch(key))
    new_piece = piece.transpose(i)
    return new_piece


def flatten(l):
    return [item for sublist in l for item in sublist]
