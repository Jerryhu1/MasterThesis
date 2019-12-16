from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFrame


class PlayControlBar(QFrame):
    def __init__(self, toNext, play, toPrevious):
        super().__init__()
        self.toNext = toNext
        self.play = play
        self.toPrevious = toPrevious
        self.initUI()
        self.setStyleSheet("""
            QFrame {
                background-color: #3A3A3A;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #f2f2f2;
                border: 1px solid #f2f2f2;
                max-width: 50px;
                min-height: 20px;
            }
            
            QPushButton:pressed {
                color: #7A7A7A;
                border: 1px solid #7A7A7A;
            }
                        
        """)


    def initUI(self):
        hbox = QHBoxLayout()

        prevBtn = QPushButton("Previous")
        prevBtn.clicked.connect(self.toPrevious)
        playPauseBtn = QPushButton("Play")
        playPauseBtn.clicked.connect(self.play)
        nextBtn = QPushButton("Next")
        nextBtn.clicked.connect(self.toNext)
        hbox.addWidget(prevBtn)
        hbox.addWidget(playPauseBtn)
        hbox.addWidget(nextBtn)
        self.setLayout(hbox)

