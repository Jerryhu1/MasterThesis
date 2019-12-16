from PyQt5.QtCore import QThread

from ea import musicPlayer


class MusicPlayerThread(QThread):
    def __init__(self, piece, musicType):
        QThread.__init__(self)
        self.piece = piece
        self.musicType = musicType

    def run(self):
        if self.musicType == 'measure':
            musicPlayer.play_measure(self.piece)
        elif self.musicType == 'piece':
            musicPlayer.play(self.piece)
        else:
            print('No music type was given to the music thread')