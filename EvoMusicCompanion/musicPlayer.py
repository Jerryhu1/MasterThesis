from music21 import *


def play(population):
    population = map(lambda x: x[0], population)

    notes = []
    for i in population:
        measure = []
        print(i)
        for j in i:
            if j[0] == ' ':
                n = note.Rest()
                n.duration.type = j[1]
                measure.append(n)
            else:
                n = note.Note(j[0])
                n.duration.type = j[1]
                measure.append(n)
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
