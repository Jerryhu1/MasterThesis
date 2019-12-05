from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        titleLabel = QLabel(text="EvoMusic")
        generationsLabel = QLabel(text="Generation: 1")
        instructionsButton = QPushButton("Help")
        vbox.addWidget(titleLabel)
        vbox.addWidget(generationsLabel)
        vbox.addWidget(instructionsButton)
        vbox.addStretch(1)
        self.setLayout(vbox)