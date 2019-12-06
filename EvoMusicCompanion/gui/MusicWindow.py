from functools import partial

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QHBoxLayout

from ea import musicPlayer
from gui.MusicPlayerThread import MusicPlayerThread
from gui.PlayControlBar import PlayControlBar
from gui.models.MusicWindowViewModel import MusicWindowViewModel
from music21 import midi


class MusicWindow(QWidget):

    def __init__(self, model: MusicWindowViewModel):
        super().__init__()
        self.model = model
        self.titleLabel = QLabel(text=f"Piece: {self.model.curr_piece_idx + 1}/{len(self.model.individuals)}")
        self.initUI()
        self.musicThread = MusicPlayerThread(None, '')

    def setModel(self, model):
        self.model = model

    def initUI(self):
        vbox = QVBoxLayout()

        fullbox = QHBoxLayout()
        fullbox_container = QVBoxLayout()
        fullPlayBtn = QPushButton("Play full")
        fullPlayBtn.clicked.connect(self.playPiece)
        fullboxRating = QHBoxLayout()
        fullbox_container.addWidget(fullPlayBtn)
        fullbox_container.addLayout(fullboxRating)
        fullbox_container.setContentsMargins(200, 0, 200, 0)
        fullbox.addLayout(fullbox_container)

        for i in range(5):
            ratingBtn = QPushButton()
            ratingBtn.clicked.connect(partial(self.setPieceRating, self.model.curr_piece_idx, i))
            fullboxRating.addWidget(ratingBtn)

        measures = self.model.curr_individual.measures
        measureGrid = QGridLayout()

        for m in range(len(measures)):
            measureBtn = QPushButton(f"Measure {m+1}", self)
            measureBtn.clicked.connect(partial(self.playMeasure, m))
            measureGrid.addWidget(measureBtn, 0, m)
            ratingWidget = QWidget()
            ratingLayout = QHBoxLayout()

            for i in range(5):
                ratingBtn = QPushButton()
                ratingBtn.clicked.connect(partial(
                    self.setMeasureRating, self.model.curr_piece_idx, m, i))
                ratingLayout.addWidget(ratingBtn)

            ratingWidget.setLayout(ratingLayout)
            measureGrid.addWidget(ratingWidget, 1, m)

        pcb = PlayControlBar(self.toNextPiece, self.toPreviousPiece)
        vbox.addWidget(self.titleLabel, 1)
        vbox.addLayout(fullbox, 1)
        vbox.addLayout(measureGrid, 4)
        vbox.addWidget(pcb, 1)

        self.setLayout(vbox)

    def setPieceRating(self, pieceIndex, rating):
        print(f"Set piece {pieceIndex} to rating: {rating}")
        self.model.parent.setPieceRating(pieceIndex, rating)

    def setMeasureRating(self, pieceIndex, measureIndex, rating):
        print(f"Set measure {measureIndex} to rating: {rating} of piece: {pieceIndex}")
        self.model.parent.setMeasureRating(pieceIndex, measureIndex, rating)

    def playMeasure(self, measure_idx):
        self.musicThread.terminate()
        measure = self.model.curr_individual.measures[measure_idx]
        self.musicThread = MusicPlayerThread(measure, 'measure')
        self.musicThread.start()

    def playPiece(self):
        self.musicThread.terminate()
        self.musicThread = MusicPlayerThread([self.model.curr_individual], 'piece')
        self.musicThread.start()

    def toNextPiece(self):
        next_index = self.model.curr_piece_idx + 1
        if next_index < len(self.model.individuals):
            self.model.curr_individual = self.model.individuals[next_index]
            self.model.curr_piece_idx = next_index
            self.refreshTitleLabel()

    def toPreviousPiece(self):
        next_index = self.model.curr_piece_idx - 1

        if next_index >= 0:
            self.model.curr_individual = self.model.individuals[next_index]
            self.model.curr_piece_idx = next_index
            self.refreshTitleLabel()

    def toPieceByIdx(self, index):
        self.model.curr_individual = self.model.individuals[index]
        self.refreshTitleLabel()

    def refreshTitleLabel(self):
        print(f"Curr index: {self.model.curr_piece_idx}")
        self.titleLabel.setText(f"Piece: {self.model.curr_piece_idx + 1}/{len(self.model.individuals)}")
        self.update()