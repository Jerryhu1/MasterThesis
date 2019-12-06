from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QHBoxLayout, QMainWindow

from ea import modelTrainer
from ea.duration import Duration
from ea.individual import Individual, Measure, Note
from ea.simulation import Simulation
from gui.MusicWindow import MusicWindow
from gui.Sidebar import Sidebar
from gui.models.MusicWindowViewModel import MusicWindowViewModel


class Main(QWidget):

    def __init__(self):
        super().__init__()
        simulation = Simulation(0.5, 10)
        simulation.run_interactively()
        self.state = MainState(simulation)
        self.music_window = None
        self.sidebar = None
        self.main_container = None
        self.initWidgets()
        self.initMainContainer()
        self.initUI()

    def initWidgets(self):
        population = self.state.simulation.population
        self.music_window = MusicWindow(MusicWindowViewModel(self, population))
        self.sidebar = Sidebar(self)

    def initMainContainer(self):
        self.main_container = QHBoxLayout()
        self.main_container.addWidget(self.sidebar, 1)
        self.main_container.addWidget(self.music_window, 4)

    def initUI(self):
        self.setLayout(self.main_container)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('EvoMusic')
        self.show()

    # def closeEvent(self, event):
    #
    #     reply = QMessageBox.question(self, 'Message',
    #                                  "Are you sure you want to quit?", QMessageBox.Yes |
    #                                  QMessageBox.No, QMessageBox.No)
    #
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initPopulation(self):
        corpus = modelTrainer.get_corpus()
        pitch_matrix = modelTrainer.train_pitch_matrix(corpus)
        duration_matrix = modelTrainer.train_duration_matrix(corpus)
        self.simulation.run_interactively(pitch_matrix, duration_matrix, None)

    def toNextGeneration(self):
        self.state.simulation.update()
        self.state.currGeneration += 1
        self.updateViews()

    def updateViews(self):
        musicViewModel = MusicWindowViewModel(self, self.state.simulation.population, None, None)
        self.main_container.removeWidget(self.music_window)
        self.main_container.removeWidget(self.sidebar)

        self.music_window = MusicWindow(musicViewModel)
        self.sidebar = Sidebar(self, self.state.currGeneration)
        self.initMainContainer()
        self.update()

    def setPieceRating(self, piece_idx, rating):
        self.state.simulation.population[piece_idx].user_score = rating

    def setMeasureRating(self, piece_index, measure_index, rating):
        self.state.simulation.population[piece_index]\
            .measures[measure_index].user_score = rating


class MainState:
    def __init__(self, simulation: Simulation):
        self.currGeneration: int = 1
        self.simulation: Simulation = simulation
        self.metrics: Metrics = Metrics()


class Metrics:
    def __init__(self):
        self.allRatings = []
        self.timeElapsed = 0


testIndividual = Individual(
    measures=[
        Measure(
            [
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5))
            ], 0, None),
        Measure(
            [
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5))
            ], 0, None)
    ], fitness=0
)
