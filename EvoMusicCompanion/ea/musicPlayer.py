from music21 import note, chord, stream, duration, interval, midi
from ea import individual
from ea.individual import Measure, Note


def play(population: [individual.Individual]):
    s = getPopulationScore(population)
    player = midi.realtime.StreamPlayer(s)
    player.play()


def play_music_xml(population: [individual.Individual]):
    s = getPopulationScore(population)
    s.show('musicxml')


def getPopulationScore(population: [individual.Individual]):
    s = stream.Score(id='mainScore')
    part = stream.Part(id='part0')
    part1 = stream.Part(id='part1')
    for i in range(len(population)):
        # For each measure
        for m in population[i].measures:
            measure = stream.Measure()
            chord_measure = stream.Measure()
            if m.chord is not None:
                chord_measure.append(chord.Chord(m.chord, quarterLength=4.0))
            duration_count = 0.0
            # For each note
            for j in m.notes:
                if j.pitch == 'REST':
                    n = note.Rest()
                    n.duration = duration.Duration(quarterLength=j.duration.duration_value / 0.25)
                else:
                    n = note.Note(j.pitch)
                    n.duration = duration.Duration(quarterLength=j.duration.duration_value / 0.25)
                measure.append(n)
                duration_count += j.duration.duration_value
            # Add rest if measure is not filled
            if duration_count < 1.0:
                measure[len(measure)-1].duration.quarterLength += (1.0 - duration_count) / 0.25

            part.append(measure)
            part1.append(chord_measure)
    s.append(part)
    s.append(part1)
    return s


def play_intervals(population: [individual.Individual]):
    population = map(lambda x: x.notes, population)
    score = []

    for i in population:
        # For each measure
        for m in i:
            measure = []
            # For each note
            for j in m:
                if j.pitch == 'REST':
                    n = note.Rest()
                    n.duration = duration.Duration(quarterLength=j.duration.duration_value / 0.25)
                    measure.append(n)
                else:
                    intv = interval.Interval(j.interval)
                    n = intv.transposeNote(note.Note('C5'))
                    n.duration = duration.Duration(quarterLength=j.duration.duration_value / 0.25)
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
    chords = get_c_chord_part(len(part))
    s.append(part)
    s.append(chords)

    print(f'key = {s.analyze("key")}')

    player = midi.realtime.StreamPlayer(s)

    player.play()


def get_c_chord_part(measures):
    chords = [['C3', 'E3', 'G3'], ['G3', 'B3', 'D3'], ['E3', 'G3', 'B3'], ['D3', 'F#3', 'A3']]
    counter = 0
    chord_part = stream.Part(id='part1')
    for m in range(measures):

        c = chord.Chord(chords[counter], quarterLength=4.0)
        chord_part.append(c)
        counter += 1
        if counter == 4:
            counter = 0

    return chord_part


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


def play_measure(measure: Measure):
    s = stream.Score(id="mainScore")

    notes_part = stream.Part(id="part0")
    m = convert_measure_to_music21_measure(measure)
    notes_part.append(m)
    s.append(notes_part)

    print(measure.chord)
    chord_part = stream.Part(id="part1")
    chord_measure = stream.Measure(1)
    chord_measure.append(chord.Chord(measure.chord, quarterLength=4.0))
    chord_part.append(chord_measure)
    s.append(chord_part)

    player = midi.realtime.StreamPlayer(s)
    player.play()


def convert_measure_to_music21_measure(m: Measure):
    m.notes: [Note]
    measure = stream.Measure(1)
    for j in m.notes:
        if j.pitch == 'REST':
            n_1 = note.Rest()
            n_1.duration = duration.Duration(quarterLength=j.duration.duration_value / 0.25)
        else:
            n_1 = note.Note(j.pitch)
            n_1.duration = duration.Duration(quarterLength=j.duration.duration_value / 0.25)
        measure.append(n_1)

    return measure
