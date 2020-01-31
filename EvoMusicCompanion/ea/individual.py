from ea import constants, util
import music21
import re


class Individual:
    user_score = 3

    def __init__(self, measures, fitness, fitnesses = None):
        self.measures = measures
        self.fitness = fitness
        self.fitnesses = fitnesses

    def __str__(self):
        return f"fitness: {self.fitness}, Measures: {self.measures} \n"

    __repr__ = __str__

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_total_duration(self):
        dur = [j.duration for j in [i for i in self.notes]]
        return sum(constants.flatten(dur))

    def get_flattened_notes(self):
        notes = list(map(lambda x: x.notes, self.measures))
        return util.flatten(notes)

    def get_notes_per_measure(self):
        return list(map(lambda x: x.notes, self.measures))


class Note:

    def __init__(self, pitch, duration, interval=None, interval_root=None):
        self.pitch = pitch
        self.pitchWithoutOctave = re.sub('\d+', '', pitch)
        self.duration = duration
        self.interval = interval
        self.interval_root = interval_root

    def __str__(self):
        return f"({self.pitch}, {self.duration})"

    __repr__ = __str__

    def __gt__(self, other):
        return music21.note.Note(self.pitch) > music21.note.Note(other.pitch)

    def to_music21_note(self) -> music21.note.Note:
        n = music21.note.Note(self.pitch)
        n.duration = music21.duration.Duration(self.duration.duration_value / 0.25)
        return n

    def set_pitch(self, pitch):
        self.pitch = pitch
        if pitch != "REST":
            self.pitchWithoutOctave = re.sub('\d+', '', pitch)
        else:
            self.pitchWithoutOctave = "REST"


class Measure:
    user_score = 3

    def __init__(self, notes, fitness, chord):
        self.notes = notes
        self.fitness = fitness
        self.chord = chord
        if chord is not None and len(chord) != 0:
            self.chordWithoutOctave = list(map(lambda x: re.sub('\d+', '', x), chord))
        else:
            self.chordWithoutOctave = []

    def set_chord(self, chord):
        self.chord = chord
        if chord is not None and len(chord) != 0:
            self.chordWithoutOctave = list(map(lambda x: re.sub('\d+', '', x), chord))

    def get_total_duration(self):
        counter = 0.0
        for n in self.notes:
            counter += n.duration.duration_value
        return counter

    def __str__(self):
        return f"Notes: {self.notes}, Chord: {self.chord} \n"

    __repr__ = __str__
