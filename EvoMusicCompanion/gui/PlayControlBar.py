from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class PlayControlBar(QWidget):
    def __init__(self, toNext, toPrevious):
        super().__init__()
        self.toNext = toNext
        self.toPrevious = toPrevious
        self.initUI()


    def initUI(self):
        hbox = QHBoxLayout()

        prevBtn = QPushButton("|<")
        prevBtn.clicked.connect(self.toPrevious)
        playPauseBtn = QPushButton("|>")
        nextBtn = QPushButton(">|")
        nextBtn.clicked.connect(self.toNext)
        hbox.addWidget(prevBtn)
        hbox.addWidget(playPauseBtn)
        hbox.addWidget(nextBtn)
        self.setLayout(hbox)

