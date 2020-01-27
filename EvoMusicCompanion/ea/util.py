from music21 import interval, pitch


def transpose_piece(piece, key):
    k = piece.analyze('key')
    if k.tonicPitchNameWithCase.islower():
        return None

    i = interval.Interval(k.tonic, pitch.Pitch(key))
    new_piece = piece.transpose(i)
    return new_piece


def flatten(l):
    return [item for sublist in l for item in sublist]


