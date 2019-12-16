from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QHBoxLayout, QMainWindow

from ea import modelTrainer, musicPlayer
from ea.duration import Duration
from ea.individual import Individual, Measure, Note
from ea.simulation import Simulation
from gui.MusicPlayerThread import MusicPlayerThread
from gui.MusicWindow import MusicWindow
from gui.Sidebar import Sidebar
from gui.models.MusicWindowViewModel import MusicWindowViewModel
from gui.stylesheet import main as style


class Main(QWidget):

    def __init__(self):
        super().__init__()
        simulation = Simulation(0.5, 100)
        simulation.run_interactively()
        self.state = MainState(simulation)
        self.music_window: QWidget = None
        self.music_thread = MusicPlayerThread(None, '')
        self.sidebar = None
        self.main_container: QHBoxLayout = None
        self.setStyleSheet(style.main)
        self.initWidgets()
        self.initMainContainer()
        self.initUI()

    def restart(self):
        self.__init__()

    def initWidgets(self):
        population = self.state.simulation.population[0:self.state.simulation.selection_size]
        self.music_window = MusicWindow(MusicWindowViewModel(self, population))
        self.sidebar = Sidebar(self)

    def initMainContainer(self):
        self.main_container = QHBoxLayout()
        self.main_container.setContentsMargins(0, 0, 0, 0)
        self.main_container.setSpacing(0)
        self.main_container.addWidget(self.sidebar, 1)
        self.main_container.addWidget(self.music_window, 4)

    def initUI(self):
        self.setLayout(self.main_container)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('EvoMusic')
        self.setObjectName('main')
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
        print(f"Generating next generation {self.state.currGeneration + 1}")
        self.state.simulation.update()
        self.state.currGeneration += 1
        self.state.curr_piece_index = 0
        self.state.curr_pieces = self.state.simulation.population[0:5]
        self.updateViews()

    def updateViews(self):
        self.main_container.removeWidget(self.music_window)
        self.music_window.deleteLater()
        musicViewModel = MusicWindowViewModel(self,
                                              self.state.curr_pieces,
                                              self.state.curr_pieces[self.state.curr_piece_index]
                                              , None)

        self.music_window = MusicWindow(musicViewModel)
        self.main_container.addWidget(self.music_window)
        self.sidebar.setModel(self.state.currGeneration)
        self.update()

    def setPieceRating(self, piece_idx, rating):
        self.state.simulation.population[piece_idx].user_score = rating

    def setMeasureRating(self, piece_index, measure_index, rating):
        self.state.simulation.population[piece_index] \
            .measures[measure_index].user_score = rating

    def playMusicXml(self):
        curr = self.music_window.model.curr_piece
        musicPlayer.play_music_xml([curr])

    def toNextPiece(self):
        next_index = self.state.curr_piece_index + 1
        if next_index < len(self.state.curr_pieces):
            self.state.curr_individual = self.state.curr_pieces[next_index]
            self.state.curr_piece_index += 1
            self.updateViews()

    def toPreviousPiece(self):
        prev_index = self.state.curr_piece_index - 1
        if prev_index >= 0:
            self.state.curr_individual = self.state.curr_pieces[prev_index]
            self.state.curr_piece_index -= 1
            self.updateViews()

    def refreshWindows(self):
        self.main_container.removeWidget(self.main_container)
        self.music_window.deleteLater()
        self.main_container.addWidget()

    def play(self):
        self.music_thread.terminate()
        self.music_thread = MusicPlayerThread([self.state.curr_pieces[self.state.curr_piece_index]], 'piece')
        self.music_thread.start()


class MainState:
    def __init__(self, simulation: Simulation):
        self.currGeneration: int = 1
        self.simulation: Simulation = simulation
        self.curr_pieces = simulation.population[0:5]
        self.curr_piece_index = 0
        self.musicThread = MusicPlayerThread(None, '')


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
