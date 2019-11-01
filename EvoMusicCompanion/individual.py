import constants
import music21

class Individual:

    def __init__(self, notes, fitness):
        self.notes = notes
        self.fitness = fitness

    def __str__(self):
        return f"Notes: {self.notes} fitness: {self.fitness}"

    __repr__ = __str__

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_total_duration(self):
        dur = [j.duration for j in [i for i in self.notes]]
        return sum(constants.flatten(dur))


class Note:

    def __init__(self, pitch, duration):
        self.pitch = pitch
        self.duration = duration

    def __str__(self):
        return f"({self.pitch}, {self.duration})"

    __repr__ = __str__

    def __gt__(self, other):
        music21.note.Note(self.pitch) > music21.note.Note(other.pitch)
        
