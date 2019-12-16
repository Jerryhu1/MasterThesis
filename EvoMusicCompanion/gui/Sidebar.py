from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame

from gui.stylesheet.main import main


class Sidebar(QFrame):

    def __init__(self, parent):
        super().__init__()
        self.instructionsButton = QPushButton("Help")
        self.parent = parent
        self.generationsLabel = QLabel(text=f"Generation: 1")
        self.initUI()
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            QWidget{ 
                background-color: #2A2A2A;
            }
            QPushButton {
                background-color: #ff2345;
                color: #f3f3f3;
                font-weight: bold;
            }
            QLabel{
                color: #f3f3f3;
            }
            
            QLabel#app-title {
                font-size: 20px;
            }
        """)
        self.setContentsMargins(20, 20, 20, 20)


    def setModel(self, generation):
        self.generationsLabel.setText(f"Generation: {generation}")
        self.update()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        titleLabel = QLabel(text="EvoMusic")
        titleLabel.setObjectName('app-title')

        generateButton = QPushButton("Generate new songs")
        generateButton.clicked.connect(self.parent.toNextGeneration)

        restartButton = QPushButton("Restart")
        restartButton.clicked.connect(self.parent.restart)

        museScoreBtn = QPushButton("Play in MuseScore")
        museScoreBtn.clicked.connect(self.parent.playMusicXml)

        vbox.addWidget(titleLabel)
        vbox.addWidget(self.generationsLabel)
        vbox.addWidget(museScoreBtn)
        vbox.addWidget(generateButton)
        vbox.addWidget(self.instructionsButton)
        vbox.addWidget(restartButton)
        vbox.addStretch(1)
        self.setObjectName('sidebar')
        self.setLayout(vbox)
        self.setStyleSheet(main)

    def toNextGeneration(self):
        self.parent.toNextGeneration()
