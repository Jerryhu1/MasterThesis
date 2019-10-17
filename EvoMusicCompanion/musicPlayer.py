from music21 import *


def play(population):
    population = map(lambda x: x[0], population)

    notes = []
    for i in population:
        measure = []
        for j in i:
            if j == ' ':
                measure.append(note.Rest())
            else:
                measure.append(note.Note(j))
        notes.append(measure)

    s = stream.Score(id='mainScore')
    part = stream.Part(id='part0')

    for i in range(len(notes)):
        m = stream.Measure(i + 1)
        notesInMeasure = notes[i]
        for n in notesInMeasure:
            m.append(n)
        part.append(m)

    s.append(part)
    s.show('musicxml')
