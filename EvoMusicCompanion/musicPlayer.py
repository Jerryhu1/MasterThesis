from music21 import *

def play(population):
    # Map note strings to music21 notes
    notes = list(map(lambda x: list(map(lambda y: note.Note(y), x)), population))
    s = stream.Score(id='mainScore')
    part = stream.Part(id='part0')
    measures = []
    for i in range(len(notes)):
        m = stream.Measure(i+1)
        notesInMeasure = notes[i]
        for n in notesInMeasure:
            m.append(n)
        part.append(m)