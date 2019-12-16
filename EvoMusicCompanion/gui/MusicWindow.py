from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QHBoxLayout, QButtonGroup, \
    QRadioButton

from gui.MusicPlayerThread import MusicPlayerThread
from gui.PlayControlBar import PlayControlBar
from gui.models.MusicWindowViewModel import MusicWindowViewModel


class MusicWindow(QWidget):
    btn_colors = ['#EF1C1C', '#FF8A00', '#FFF500', '#4AD10A', '#0B8F00']

    def __init__(self, model: MusicWindowViewModel):
        super().__init__()
        self.model = model
        self.titleLabel = QLabel(text=f"Piece: {self.model.curr_piece_idx + 1}/{len(self.model.pieces)}")
        self.titleLabel.setStyleSheet("""
            font-size: 30px;
            color: #FF2345;
        """)
        self.fitnessLabel = QLabel(text=f"Fitness: {self.model.curr_piece.fitness}")
        self.initUI()
        self.musicThread = MusicPlayerThread(None, '')
        self.ratingButtons = None
        self.setStyleSheet("""
            QRadioButton#rating-btn {
                max-height: 10px;
                max-width: 10px;
                border-radius: 12px;
            }
            
            QPushButton#measure-btn {
                min-height: 100px;
                min-width:100px;
            }
            
        """)

    def setModel(self, model):
        self.model = model
        self.refreshLabels()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        measures = self.model.curr_piece.measures
        measureGrid = QGridLayout()

        for m in range(len(measures)):
            measureBtn = QPushButton(f"Measure {m + 1}", self)
            measureBtn.setObjectName('measure-btn')
            measureBtn.clicked.connect(partial(self.playMeasure, m))
            measureGrid.addWidget(measureBtn, 0, m, 1, 1, alignment=QtCore.Qt.AlignCenter)
            ratingWidget = QWidget()
            ratingLayout = QHBoxLayout()
            ratingLayout.setContentsMargins(50, 0, 50, 0)
            ratingLayout.setSpacing(20)

            button_group = QButtonGroup(ratingLayout)

            for i in range(5):
                ratingBtn = QRadioButton()

                ratingBtn.toggled.connect(partial(
                    self.setMeasureRating, self.model.curr_piece_idx, m, i + 1))

                if measures[m].user_score == i+1:
                    print(measures[m].user_score)
                    ratingBtn.setChecked(True)

                ratingBtn.setObjectName('rating-btn')
                ratingBtn.setStyleSheet(f"""
                    QRadioButton {{
                        background-color: {self.btn_colors[i]};
                        border: 8px solid {self.btn_colors[i]};
                    }}
                    
                    QRadioButton::indicator::unchecked {{
                        background-color: {self.btn_colors[i]}
                        border: none;
                    }}
                """)
                button_group.addButton(ratingBtn)
                ratingLayout.addWidget(ratingBtn)

            ratingWidget.setLayout(ratingLayout)
            measureGrid.addWidget(ratingWidget, 1, m)

        pcb = PlayControlBar(self.model.parent.toNextPiece,
                             self.model.parent.play,
                             self.model.parent.toPreviousPiece)

        vbox.addWidget(self.titleLabel, 1, QtCore.Qt.AlignCenter)
        vbox.addLayout(measureGrid, 4)
        vbox.addLayout(self.initFullBox(), 1)
        vbox.addWidget(self.fitnessLabel)
        vbox.addWidget(pcb, 0.9)
        self.setLayout(vbox)

    def initFullBox(self):
        fullbox = QHBoxLayout()
        fullbox_container = QVBoxLayout()
        fullboxRating = QHBoxLayout()
        fullbox_container.addLayout(fullboxRating)
        fullbox_container.setContentsMargins(200, 0, 200, 0)
        fullbox.addLayout(fullbox_container)
        button_group = QButtonGroup(fullbox)
        for i in range(5):
            ratingBtn = QRadioButton()
            ratingBtn.toggled.connect(partial(self.setPieceRating, self.model.curr_piece_idx, i + 1))
            if self.model.curr_piece.user_score == i+1:
                ratingBtn.setChecked(True)
            ratingBtn.setObjectName('rating-btn')
            ratingBtn.setStyleSheet(f"background-color: {self.btn_colors[i]}; "
                                    f"border: 10px solid {self.btn_colors[i]};"
                                    f"border-radius: 14px; "
                                    )
            button_group.addButton(ratingBtn)
            fullboxRating.addWidget(ratingBtn)
        return fullbox

    def setPieceRating(self, pieceIndex, rating):
        print(f"Set piece {pieceIndex} to rating: {rating}")
        self.model.parent.setPieceRating(pieceIndex, rating)

    def setMeasureRating(self, pieceIndex, measureIndex, rating):
        print(f"Set measure {measureIndex} to rating: {rating} of piece: {pieceIndex}")
        self.model.parent.setMeasureRating(pieceIndex, measureIndex, rating)

    def playMeasure(self, measure_idx):
        self.musicThread.terminate()
        measure = self.model.curr_piece.measures[measure_idx]
        self.musicThread = MusicPlayerThread(measure, 'measure')
        self.musicThread.start()

    def playPiece(self):
        self.musicThread.terminate()
        self.musicThread = MusicPlayerThread([self.model.curr_piece], 'piece')
        self.musicThread.start()

    def refreshLabels(self):
        self.refreshFitnessLabel()
        self.refreshTitleLabel()

    def refreshTitleLabel(self):
        print(f"Curr index: {self.model.curr_piece_idx}")
        self.titleLabel.setText(f"Piece: {self.model.curr_piece_idx + 1}/{len(self.model.pieces)}")

    def refreshFitnessLabel(self):
        self.fitnessLabel.setText(f"Fitness: {self.model.curr_piece.fitness}")
