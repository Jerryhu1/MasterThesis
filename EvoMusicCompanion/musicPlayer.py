from music21 import *
import individual


def play(population: [individual.Individual]):
    population = map(lambda x: x.notes, population)
    score = []

    for i in population:
        # For each measure
        for m in i:
            measure = []
            # For each note
            for j in m:
                if j.pitch == ' ':
                    n = note.Rest()
                    n.duration = duration.Duration(quarterLength=j.duration.duration_value/0.25)
                    measure.append(n)
                else:
                    n = note.Note(j.pitch)
                    n.duration = duration.Duration(quarterLength=j.duration.duration_value/0.25)
                    measure.append(n)
            score.append(measure)

    s = stream.Score(id='mainScore')
    part = stream.Part(id='part0')

    for i in range(len(score)):
        m = stream.Measure(i + 1)
        notesInMeasure = score[i]
        for n in notesInMeasure:
            m.append(n)
        part.append(m)

    s.append(part)
    s.show('musicxml')


def play_pitches(population):
    score = []
    for i in population:
        for j in i:
            score.append(note.Note(j))

    s = stream.Score(id='mainScore')
    part = stream.Part(id='part0')

    part.append(score)

    s.append(part)
    s.show('musicxml')
