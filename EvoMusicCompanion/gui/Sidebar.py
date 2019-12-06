from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class Sidebar(QWidget):

    def __init__(self, parent, generation: int = 1):
        super().__init__()
        self.instructionsButton = QPushButton("Help")
        self.parent = parent
        self.generation = generation
        self.initUI()

    def setModel(self, generation):
        self.generation = generation
        self.update()

    def initUI(self):
        vbox = QVBoxLayout()
        titleLabel = QLabel(text="EvoMusic")
        generationsLabel = QLabel(text=f"Generation: {self.generation}")
        
        generateButton = QPushButton("Generate new songs")
        generateButton.clicked.connect(self.parent.toNextGeneration)

        vbox.addWidget(titleLabel)
        vbox.addWidget(generationsLabel)
        vbox.addWidget(generateButton)
        vbox.addWidget(self.instructionsButton)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def setModel(self, generation):
        self.generation = generation
        self.update()

    def toNextGeneration(self):
        self.parent.toNextGeneration()
